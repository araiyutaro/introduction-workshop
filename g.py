import requests
import io

import spacy
from pdfminer.high_level import extract_text

announcements = [
    # ("サントリー", "https://www.suntory.co.jp/company/financial/pdf/securities_202212.pdf"),
    # ("キリン", "https://pdf.irpocket.com/C2503/xivA/YlQ7/TRjW.pdf"),
    # ("アサヒ", "https://www.asahigroup-holdings.com/ir_library_file/file/securities2022_4q.pdf"),
    # ("サッポロ", "https://www.sapporoholdings.jp/ir/library/securities_report/items/2022__12_yuho.pdf")
    ("ソニー", "https://www.sony.com/ja/SonyInfo/IR/library/r4_q4.pdf"),
    # ("エプソン", "https://corporate.epson/ja/investors/publications/pdf/securities/2022.pdf"),
    ("パナソニック", "https://holdings.panasonic/jp/corporate/investors/pdf/Report2022.pdf"),
    # ("ライオン", "https://www.suntory.co.jp/company/financial/pdf/securities_202312.pdf"),
    # ("花王", "https://www.suntory.co.jp/company/financial/pdf/securities_202312.pdf"),
    # ("ユニ・チャーム", "https://www.suntory.co.jp/company/financial/pdf/securities_202312.pdf"),
]
purpose_words = [
    "地域社会",
    "高齢者",
    "共存",
    "ダイバーシティ",
    "地域応援",
    "復興支援",
    "フェアトレード",
    "寄付",
    "人権",
    "難民",
    "支援",
    "農村開発",
    "コミュニティ",
    "平等",
    "ライフスタンス",
    "インクルーシブ",
    "元気",
    "食糧危機",
    "再生可能",
    "社会課題",
    "共創",
    "安心",
    "安全",
    "環境保全",
    "サスティナビリティ",
    "環境負荷",
    "再利用",
    "リサイクル",
    "省エネ",
    "水質保全",
    "廃棄物再資源化",
    "排出量削減",
    "水源涵養",
    "リペア",
    "リユース",
    "循環型",
    "脱炭素",
    "自然由来",
    "天然資源",
    "森林破壊",
    "地球環境",
    "リデュース",
    "エコ",
    "SDGs",
    "パーパス",
    "豊かな",
    "共感",
    "感動",
]


def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック
    return response.content


def pdf_to_text(pdf_content):
    with io.BytesIO(pdf_content) as pdf_file:
        text = extract_text(pdf_file)
    return text.replace(' ', '').replace('　', '')


def text_to_words(text):
    nlp = spacy.load("ja_ginza")
    chunk_size = 10000
    words_list = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        doc = nlp(chunk)
        for token in doc:
            if token.tag_ in ["名詞-普通名詞-一般"]:
                words_list.append(token.lemma_)
    return words_list


def get_matched_list(words):
    matched_list = []
    for word in words:
        matched_list += filter(lambda x: x in word, purpose_words)
    return matched_list


for announcement in announcements:
    company_name = announcement[0]
    url = announcement[1]
    pdf_content = download_pdf(url)
    text = pdf_to_text(pdf_content)
    words = text_to_words(text)
    print(company_name)
    print("単語数:" + str(len(words)))
    matched_list = get_matched_list(words)
    print(matched_list)
    print("パーパス文言数：" + str(len(matched_list)))
