from bs4 import BeautifulSoup

html_doc = '<a class="item-subject" href="https://123.com/bbs/board.php?bo_table=aboard01&amp;wr_id=5452"> <span class="orangered visible-xs pull-right wr-comment"> <i class="fa fa-comment lightgray"></i> <b>+41</b>    #댓글수 </span> <span class="wr-icon wr-new"></span> #새글을 알리는 아이콘           오늘의 날씨 이유        # 제목 <b class="count orangered hidden-xs">+41</b>    #댓글수 </a>, <a class="item-subject" href="https://123.com/bbs/board.php?bo_table=aboard01&amp;wr_id=5451"> <span class="orangered visible-xs pull-right wr-comment"> <i class="fa fa-comment lightgray"></i> <b>+19</b> </span> <span class="wr-icon wr-new"></span>                            날씨 너무춥네요 ㅠ <b class="count orangered hidden-xs">+19</b> </a>, <a class="item-subject" href="https://123.com/bbs/board.php?bo_table=aboard01&amp;wr_id=5454"> <span class="orangered visible-xs pull-right wr-comment"> <i class="fa fa-comment lightgray"></i> <b>+23</b> </span> <span class="wr-icon wr-new"></span>                            우한 코로나 <b class="count orangered hidden-xs">+23</b> </a>'
# print(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')

subjects = soup.select('.item-subject')  #게시글 클래스 선택
for subject in subjects:
##    print(subject.text)
##    print(type(subject.select_one('span.wr-new')))
##    print(type(subject.select_one('span.wr-newasd')))
##    print(subject.select_one('span.wr-new') is str)
    print(subject.select_one('span.wr-new')['class'])
