# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")  # 책마다 한 권씩
LOAN_DAYS = 14   # 대출 기간: 반납 기한 = 빌린 날 + 14
MAX_LOANS = 3    # 1인 최대 대출 권수


def _valid_day(day):
    """1 이상의 정수인지 확인 (True/False는 정수로 보지 않음)"""
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


def _valid_book(book_id):
    return isinstance(book_id, str) and book_id in BOOKS


def _hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False


class LibraryLoan:
    def __init__(self):
        # 대출 중인 책: book_id -> {"name": 빌린 사람, "day": 빌린 날, "due": 반납 기한}
        self.loans = {}
        # 대출 정지 기간: name -> [(시작일, 끝일), ...]  (양 끝 포함)
        self.suspensions = {}

    # ---------- 내부 도우미 ----------
    def _books_of(self, name):
        return [(b, info) for b, info in self.loans.items() if info["name"] == name]

    def _is_suspended(self, name, day):
        for start, end in self.suspensions.get(name, []):
            if start <= day <= end:
                return True
        return False

    # ---------- 대출 ----------
    def borrow(self, book_id, name, day):
        if not _valid_book(book_id):          # 1. 없는 책 번호
            return False
        if not _valid_day(day):               # 2. day가 1 이상의 정수가 아님
            return False
        if not _hashable(name):
            return False
        if book_id in self.loans:             # 3. 이미 누군가 빌려 간 책
            return False
        mine = self._books_of(name)
        if len(mine) >= MAX_LOANS:            # 4. 이미 3권 대출 중
            return False
        for _, info in mine:                  # 5. 반납 기한이 지난 책을 갖고 있음
            if day > info["due"]:
                return False
        if self._is_suspended(name, day):     # 6. 대출 정지 기간
            return False

        self.loans[book_id] = {"name": name, "day": day, "due": day + LOAN_DAYS}
        return True

    # ---------- 반납 ----------
    def return_book(self, book_id, name, day):
        if not _valid_book(book_id):
            return -1
        if not _valid_day(day):
            return -1
        info = self.loans.get(book_id)
        if info is None or info["name"] != name:   # 그 사람이 빌리고 있지 않음
            return -1
        if day < info["day"]:                       # 빌린 날보다 이른 날
            return -1

        overdue = max(0, day - info["due"])
        del self.loans[book_id]

        if overdue > 0:
            # 반납한 날부터 연체 일수만큼의 날 동안 대출 정지
            # 예: 30일째 3일 연체 반납 → 30·31·32일째 정지
            # 겹치는 기간은 합쳐지므로 '더 늦게 끝나는 쪽'을 따름 (기간을 더하지 않음)
            self.suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    # ---------- 대출 목록 ----------
    def get_loans(self, name):
        result = [(b, info["due"]) for b, info in self._books_of(name)]
        result.sort(key=lambda t: (t[1], t[0]))   # 반납 기한 순, 같으면 책 번호 순
        return result
