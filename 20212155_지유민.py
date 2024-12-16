import random
import string
import json

# 큐 클래스 정의 (Radix Sort에서 사용)
class ArrayQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.array = [None] * capacity
        self.front = 0
        self.rear = 0

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return self.front == (self.rear + 1) % self.capacity

    def enqueue(self, item):
        if not self.is_full():
            self.rear = (self.rear + 1) % self.capacity
            self.array[self.rear] = item
        else:
            print("Queue is full. Cannot enqueue.")

    def dequeue(self):
        if not self.is_empty():
            self.front = (self.front + 1) % self.capacity
            item = self.array[self.front]
            self.array[self.front] = None  # 삭제된 자리 초기화
            return item
        else:
            print("Queue is empty. Cannot dequeue.")
            return None

# 선택 정렬
def selection_sort(A, key=lambda x: x, reverse=False):
    n = len(A)
    for i in range(n-1):
        selected = i
        for j in range(i+1, n):
            if reverse:
                if key(A[j]) > key(A[selected]):
                    selected = j
            else:
                if key(A[j]) < key(A[selected]):
                    selected = j
        A[i], A[selected] = A[selected], A[i]
    return A

# 삽입 정렬
def insertion_sort(A, key=lambda x: x, reverse=False):
    n = len(A)
    for i in range(1, n):
        current = A[i]
        j = i - 1
        if reverse:
            while j >= 0 and key(A[j]) < key(current):
                A[j + 1] = A[j]
                j -= 1
        else:
            while j >= 0 and key(A[j]) > key(current):
                A[j + 1] = A[j]
                j -= 1
        A[j + 1] = current
    return A

# 퀵 정렬
def quick_sort(A, left, right, key=lambda x: x, reverse=False):
    if left < right:
        q = partition(A, left, right, key, reverse)
        quick_sort(A, left, q-1, key, reverse)
        quick_sort(A, q+1, right, key, reverse)

def partition(A, left, right, key, reverse):
    pivot = key(A[left])
    i = left + 1
    j = right

    while True:
        if reverse:
            while i <= j and key(A[i]) >= pivot:
                i += 1
            while i <= j and key(A[j]) < pivot:
                j -= 1
        else:
            while i <= j and key(A[i]) <= pivot:
                i += 1
            while i <= j and key(A[j]) > pivot:
                j -= 1

        if i <= j:
            A[i], A[j] = A[j], A[i]
        else:
            break

    A[left], A[j] = A[j], A[left]
    return j

# 계수 정렬
def counting_sort(arr):
    if not arr:
        return arr

    # Step 1: 빈도 계산
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1

    # Step 2: 누적합 계산
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Step 3: 정렬된 배열 구축
    output = [0] * len(arr)
    for num in reversed(arr):
        count[num] -= 1
        output[count[num]] = num

    return output

# 기수 정렬
def radix_sort(A):
    BUCKETS = 10
    DIGITS = 3  # 최대 3자리 수 (0~100)

    queues = []
    for _ in range(BUCKETS):
        queues.append(ArrayQueue(len(A)))

    n = len(A)
    factor = 1

    for d in range(DIGITS):
        for i in range(n):
            digit = (A[i] // factor) % BUCKETS
            queues[digit].enqueue(A[i])

        i = 0
        for b in range(BUCKETS):
            while not queues[b].is_empty():
                A[i] = queues[b].dequeue()
                i += 1

        factor *= BUCKETS

    return A

# 학생 정보 생성
def generate_students(filename='학생.txt', num_students=30):
    students = []
    for _ in range(num_students):
        name = ''.join(random.choices(string.ascii_uppercase, k=2))
        age = random.randint(18, 22)
        score = random.randint(0, 100)
        student = {"이름": name, "나이": age, "성적": score}
        students.append(student)

    # 파일에 저장
    with open(filename, 'w', encoding='utf-8') as f:
        for student in students:
            f.write(json.dumps(student, ensure_ascii=False) + '\n')

# 학생 정보 불러오기
def load_students(filename='학생.txt'):
    students = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            student = json.loads(line.strip())
            students.append(student)
    return students

# 학생 정보 출력
def print_students(students):
    print(f"{'이름':<5} {'나이':<5} {'성적':<5}")
    print("-" * 20)
    for student in students:
        print(f"{student['이름']:<5} {student['나이']:<5} {student['성적']:<5}")
    print("-" * 20)

# 정렬 함수 매핑
def sort_students(students, sort_key, algorithm, reverse=False):
    if sort_key == '이름':
        key_func = lambda x: x['이름']
    elif sort_key == '나이':
        key_func = lambda x: x['나이']
    elif sort_key == '성적':
        key_func = lambda x: x['성적']
    else:
        print("잘못된 정렬 기준입니다.")
        return students

    if algorithm == '선택 정렬':
        return selection_sort(students, key=key_func, reverse=reverse)
    elif algorithm == '삽입 정렬':
        return insertion_sort(students, key=key_func, reverse=reverse)
    elif algorithm == '퀵 정렬':
        quick_sort(students, 0, len(students)-1, key=key_func, reverse=reverse)
        return students
    elif algorithm == '기수 정렬' and sort_key == '성적':
        scores = [student['성적'] for student in students]
        sorted_scores = radix_sort(scores)
        # 학생 리스트를 정적 점수에 따라 정렬
        sorted_students = []
        score_to_students = {}
        for student in students:
            score_to_students.setdefault(student['성적'], []).append(student)
        for score in sorted_scores:
            sorted_students.append(score_to_students[score].pop(0))
        return sorted_students
    else:
        print("잘못된 정렬 알고리즘 선택 또는 지원되지 않는 정렬 기준입니다.")
        return students

# 메인 함수
def main():
    # 데이터 생성
    generate_students()

    print("생성된 학생 정보 : ")
    students = load_students()
    print_students(students)
    while True:
        print("메뉴:")
        print("1. 이름을 기준으로 정렬")
        print("2. 나이를 기준으로 정렬")
        print("3. 성적을 기준으로 정렬")
        print("4. 프로그램 종료")

        choice = input("원하는 작업을 선택하세요 (1-4) : ")

        if choice == '4':
            print("프로그램을 종료합니다.")
            break

        if choice not in ['1', '2', '3']:
            print("잘못된 선택입니다. 다시 시도해주세요.\n")
            continue

        sort_keys = {'1': '이름', '2': '나이', '3': '성적'}
        sort_key = sort_keys[choice]

        print("\n정렬 알고리즘 선택:")
        print("1. 선택 정렬")
        print("2. 삽입 정렬")
        print("3. 퀵 정렬")
        if sort_key == '성적':
            print("4. 기수 정렬")
        algo_choice = input("원하는 정렬 알고리즘을 선택하세요: ")

        algo_map = {
            '1': '선택 정렬',
            '2': '삽입 정렬',
            '3': '퀵 정렬',
            '4': '기수 정렬'
        }

        if sort_key != '성적' and algo_choice in ['4']:
            print("성적 기준으로만 기수 정렬을 사용할 수 있습니다.")
            continue
        if algo_choice not in algo_map:
            print("잘못된 정렬 알고리즘 선택입니다. 다시 시도해주세요.\n")
            continue

        algorithm = algo_map[algo_choice]

        order = input("정렬 순서를 선택하세요 (오름차순: 1, 내림차순: 2): ")
        if order == '1':
            reverse = False
        elif order == '2':
            reverse = True
        else:
            print("잘못된 정렬 순서 선택입니다. 기본값(오름차순)으로 설정됩니다.")
            reverse = False

        # 정렬 수행
        sorted_students = sort_students(students, sort_key, algorithm, reverse)

        print("\n정렬된 학생 성적:")
        print_students(sorted_students)
        print("\n")

if __name__ == "__main__":
    main()
