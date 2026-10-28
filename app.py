# 도서관 대출 웹페이지 (Streamlit)
# ⭐ 대출 규칙은 여기 만들지 않고, solution.py의 LibraryLoan을 그대로 불러 씁니다.
import streamlit as st
from solution import LibraryLoan

st.set_page_config(page_title="도서관 대출 시스템", page_icon="📚")

# 앞에서 한 대출을 기억하도록, 화면이 새로고침돼도 같은 LibraryLoan 객체를 계속 씁니다.
if "lib" not in st.session_state:
    st.session_state.lib = LibraryLoan()
    st.session_state.log = []
lib = st.session_state.lib


def show_result(ok, msg):
    if ok:
        st.success(msg)
    else:
        st.markdown(
            f"<div style='background:#d32f2f;color:white;padding:14px;border-radius:8px;"
            f"font-size:28px;font-weight:800;text-align:center'>❌ 실패</div>"
            f"<p style='color:#d32f2f;text-align:center'>{msg}</p>",
            unsafe_allow_html=True,
        )


def to_day(text):
    """입력칸 글자를 숫자로 바꿔서 solution.py에 넘김 (검사는 solution.py가 함)"""
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)   # 2.5 같은 값도 그대로 넘겨서 solution.py가 거절하게 함
        except ValueError:
            return text


st.title("📚 도서관 대출 시스템")
st.caption("책: B001 · B002 · B003 · B004 · B005 / 대출 기간 14일 / 1인 3권까지")

tab1, tab2, tab3 = st.tabs(["대출", "반납", "대출 목록"])

with tab1:
    with st.form("borrow"):
        b = st.text_input("책 번호", placeholder="B001")
        n = st.text_input("이름", placeholder="김민수")
        d = st.text_input("며칠째", placeholder="1")
        if st.form_submit_button("대출하기", use_container_width=True):
            ok = lib.borrow(b.strip(), n.strip(), to_day(d))
            st.session_state.log.append(f"대출 {n} {b} {d}일째 → {'성공' if ok else '실패'}")
            show_result(ok, f"✅ 성공: {n.strip()}님이 {b.strip()}을(를) 빌렸습니다." if ok
                        else "대출이 거절되었습니다.")

with tab2:
    with st.form("return"):
        b = st.text_input("책 번호", placeholder="B001", key="rb")
        n = st.text_input("이름", placeholder="김민수", key="rn")
        d = st.text_input("며칠째", placeholder="10", key="rd")
        if st.form_submit_button("반납하기", use_container_width=True):
            late = lib.return_book(b.strip(), n.strip(), to_day(d))
            ok = late != -1
            st.session_state.log.append(f"반납 {n} {b} {d}일째 → {'연체 ' + str(late) + '일' if ok else '실패'}")
            show_result(ok, f"✅ 반납 성공 — 연체 {late}일" if ok else "반납이 거절되었습니다.")

with tab3:
    with st.form("loans"):
        n = st.text_input("이름", placeholder="김민수", key="ln")
        if st.form_submit_button("대출 목록 보기", use_container_width=True):
            loans = lib.get_loans(n.strip())
            if loans:
                st.write(f"**{n.strip()}** 님이 빌린 책 (반납 기한 순)")
                st.table([{"책 번호": bid, "반납 기한": f"{due}일째까지"} for bid, due in loans])
            else:
                st.info("빌린 책이 없습니다.")

st.divider()
with st.expander("기록 / 처음 상태로 되돌리기"):
    for line in st.session_state.log:
        st.write("•", line)
    if st.button("처음 상태로 초기화"):
        st.session_state.lib = LibraryLoan()
        st.session_state.log = []
        st.rerun()
