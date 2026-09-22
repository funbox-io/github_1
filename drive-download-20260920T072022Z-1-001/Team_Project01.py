import requests
# 호출 url 작성
import json
import csv


url="""http://data4library.kr/api/loanItemSrch?authKey=2e6611f2863b2d318233d7cc1506394ae28d8b28de7b56aca7c584a0b814fa4e&startDt=2025-01-01&endDt=2026-06-30&age=20&format=json"""


print("Type:",type(url))

# 인기 대출 도서 정보 요청하고 결과값 가져오기
data = requests.get(url).text
print(f'결과값: \n{data}')

# 전달받은 데이터의 자료형 확인
print(f'API 호출의 결과값의 자료형: {type(data)}')

# json 문자열 -> python dict 자료형으로 변환
dict_data = json.loads(data)
print(f'변환된 결과값: \n{dict_data}')
print('-'*80)
print(f'변환된 결과값의 자료형: {type(dict_data)}')

'''
# 결과물 -> 중첩된 구조 -> 가장 바깥쪽 {} 기준 -> key 추출
first_keys = dict_data.keys()
print(f'가장 바깥쪽 중괄호 기준으로 추출한 key: \n{first_keys}')

# 가장 바깥쪽 {} 기준으로 추출한 첫 번째 key에 매핑된 값 추출 
first_values = dict_data.get('response')
print(f'첫 번째 추출한 key에 매핑되는 값: \n{first_values}')
'''

# 중첩된 JSON 구조 확인 함수
def show_json(data, path="root", max_items=3):
    
    # 딕셔너리인 경우
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}"

            print(
                f"{new_path} → "
                f"키: {key}, "
                f"값의 자료형: {type(value).__name__}"
            )

            # 현재 값의 내부 구조도 같은 방식으로 계속 확인(재귀 호출)
            show_json(value, new_path, max_items)

    # 리스트인 경우
    elif isinstance(data, list):
        print(f"{path} → 리스트 항목 개수: {len(data)}")

        # 데이터가 너무 많으면 앞의 3개만 확인
        for index, value in enumerate(data[:max_items]):
            new_path = f"{path}[{index}]"

            print(
                f"{new_path} → "
                f"값의 자료형: {type(value).__name__}"
            )

            # 리스트 항목의 내부 구조도 같은 방식으로 계속 확인(재귀 호출)
            show_json(value, new_path, max_items)

        if len(data) > max_items:
            print(f"{path} → 나머지 {len(data) - max_items}개 생략")

    # 문자열, 숫자, True, False, None인 경우
    else:
        print(f"{path} = {data}")


# 전체 JSON 구조 확인
#show_json(dict_data)
show_json(dict_data, max_items=5000)


# JSON 응답에서 실제 도서 목록 추출
docs = dict_data["response"]["docs"]
book_list = []

for item in docs:
    # doc 딕셔너리 하나가 CSV 파일의 한 행이 됨
    book_list.append(item["doc"])


# 추출한 도서 목록을 CSV 파일로 저장
if book_list:
    #to_csv()
    with open("loan_items.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=book_list[0].keys())

        # 첫 번째 행에 딕셔너리의 키를 열 이름으로 작성
        writer.writeheader()

        # 도서 딕셔너리를 CSV에 한 행씩 작성
        writer.writerows(book_list)

    print(f"loan_items.csv 파일 저장 완료: {len(book_list)}개")
else:
    print("CSV에 저장할 도서 데이터가 없습니다.")

