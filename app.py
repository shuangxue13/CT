import streamlit as st
import json
import os
import numpy as np
from datetime import datetime

DATA = "tracer_data.json"
EMB = "event_embeddings.json"

# ---------- 工具 ----------
def load():
    if not os.path.exists(DATA):
        return []
    with open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def refine(event):
    r = dict(event)
    r["created_at"] = datetime.now().isoformat(timespec="seconds")
    c = r.get("content", "")
    r["content"] = c.strip()[:120]
    for k in ("action_taken", "result"):
        if r.get(k) == "":
            r[k] = None
    if "tags" not in r or not isinstance(r["tags"], list):
        r["tags"] = []
    return r

def template_insight(events):
    if len(events) < 2:
        return "样本不足，无法生成洞察。"
    a, b = events[0], events[1]
    return (f"你在「{a.get('context','?')}」经历 {a.get('event_type','?')}：「{a.get('content','')}」；"
            f"而在「{b.get('context','?')}」获得 {b.get('event_type','?')}：「{b.get('content','')}」。"
            f"暗示：情绪常是信号，洞察是其转化后的杠杆。")

def cos(a, b):
    a, b = np.array(a), np.array(b)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0
    return np.dot(a, b) / (na * nb)

# ---------- 页面 ----------
st.set_page_config(page_title="Consciousness Tracer", layout="wide")
st.title("🧠 Consciousness Tracer · Week 3 全集")

menu = st.sidebar.selectbox("导航",
    ["时间轴", "打标", "记录事件", "检索", "周报", "导出 MD"])

data = load()

# ---- 1 时间轴 ----
if menu == "时间轴":
    st.header("📜 时间轴（带标签）")
    for e in sorted(data, key=lambda x: x.get("created_at","")):
        tags = " ".join(e.get("tags",[]))
        st.markdown(f"**[{e.get('created_at','?')}]** `{e['event_type']}` {tags}  \n{e.get('content','')[:80]}")

# ---- 2 打标 ----
elif menu == "打标":
    st.header("🏷️ 事件打标（人工过目）")
    for i, e in enumerate(data):
        with st.expander(f"#{i+1} [{e.get('created_at','?')}] {e['event_type']}"):
            st.write(e.get('content',''))
            cur = [t.replace("#","") for t in e.get("tags",[])]
            tags = st.multiselect("标签", ["杠杆","情绪","代码","洞察","实习","废话"], default=cur, key=i)
            if st.button("确认保存", key=f"s{i}"):
                e["tags"] = ["#"+t for t in tags]
                save(data)
                st.success("已提炼入库")

# ---- 3 记录事件（Day 4） ----
elif menu == "记录事件":
    st.header("📝 记录新事件（人工过目后入库）")
    with st.form("new_ev"):
        etype = st.selectbox("类型", ["THOUGHT","EMOTION","ACTION","INSIGHT"])
        content = st.text_area("内容")
        intensity = st.slider("强度", 1, 10, 5)
        context = st.text_input("场景")
        action = st.text_input("行动")
        result = st.text_input("结果")
        tags = st.multiselect("标签", ["杠杆","情绪","代码","洞察","实习","废话"])
        submitted = st.form_submit_button("预览提炼")
    if submitted:
        raw = {"event_type":etype, "content":content, "intensity":intensity,
               "context":context, "action_taken":action, "result":result}
        refined = refine(raw)
        refined["tags"] = ["#"+t for t in tags]
        st.subheader("拟入库内容")
        st.json(refined)
        if st.button("确认入库此事件"):
            data.append(refined)
            save(data)
            st.success("事件已入库")

# ---- 4 检索 + 洞察（Day 2/3） ----
elif menu == "检索":
    st.header("🔍 聚焦式检索 + 洞察生成")
    try:
        if not os.path.exists(EMB):
            st.warning("先跑 embedder.py")
            st.stop()
        with open(EMB, "r", encoding="utf-8") as f:
            emb_data = json.load(f)
        enumerated = list(enumerate(data))
        sorted_enum = sorted(enumerated, key=lambda ix: ix[1].get("created_at",""))
        opts = [f"#{i+1} [{e.get('created_at','?')[:16]}] {e['event_type']}: {e.get('content','')[:40]}"
                for i,e in sorted_enum]
        sel = st.selectbox("选择查询事件", range(len(opts)), format_func=lambda i: opts[i])
        idx, qev = sorted_enum[sel]

        if idx >= len(emb_data):
            st.error("向量库不匹配，重跑 embedder")
            st.stop()
        qvec = emb_data[idx]["embedding"]

        hits = []
        for i,it in enumerate(emb_data):
            if i == idx: continue
            hits.append((cos(qvec, it["embedding"]), it["event"]))
        hits.sort(key=lambda x:x[0], reverse=True)

        st.subheader(f"与「{qev['event_type']}: {qev.get('content','')[:40]}」相似的：")
        for sc,ev in hits[:5]:
            st.markdown(f"**[{sc:.3f}]** `{ev.get('event_type','')}` {ev.get('content','')[:80]}")

        if len(hits)>=2:
            if st.button("基于此生成洞察"):
                insight_text = template_insight([hits[0][1], hits[1][1]])
                st.info(insight_text)
                if st.button("确认将此洞察入库"):
                    ai = {
                        "event_type":"INSIGHT_AUTO",
                        "content": insight_text,
                        "intensity":5,
                        "context":"ui_retrieve",
                        "action_taken":None,
                        "result":None,
                        "tags":["#自动洞察"],
                        "created_at": datetime.now().isoformat(timespec="seconds")
                    }
                    data.append(ai)
                    save(data)
                    st.success("INSIGHT_AUTO 已入库")
    except Exception as e:
        st.error(f"检索异常：{e}")

# ---- 5 周报 ----
elif menu == "周报":
    st.header("📊 每周聚合（主动触发）")
    insights = [e for e in data if e["event_type"] in ("INSIGHT","INSIGHT_AUTO")]
    st.metric("洞察数", len(insights))
    if st.button("生成周报并入库"):
        rep = {
            "event_type":"WEEKLY_REPORT",
            "content": f"Week items={len(data)} insights={len(insights)}",
            "intensity":None,
            "context":"ui_weekly",
            "action_taken":None,
            "result":None,
            "tags":["#周报"],
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        data.append(rep)
        save(data)
        st.success("周报已人工确认入库")

# ---- 6 导出 MD ----
elif menu == "导出 MD":
    st.header("📝 按需导出 Markdown")
    if st.button("生成 export.md"):
        md = f"# Tracer 导出\n{datetime.now()}\n\n"
        for e in sorted(data, key=lambda x:x.get("created_at","")):
            mt = " ".join(e.get("tags",[]))
            md += f"### [{e.get('created_at','?')}] {e['event_type']} {mt}\n{e.get('content','')}\n\n"
        with open("export.md","w",encoding="utf-8") as f:
            f.write(md)
        st.success("export.md 已落盘")

st.caption("所有写盘操作均需人工点击确认 · 外部大脑 Week 3 收官")