import requests
import re
import time

cookie="966C1730B2B8118F99705A2B91E32540"
session=requests.Session()

header={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "cookie":f"semester.id=242; pageSize=150; JSESSIONID={cookie}"
}


def get_Course():
    url="https://jiaowu.cqmu.edu.cn:8080/eams/evaluateStdByCourseOrTeacher!search.action"
    data={
        "semester.id":"242"
    }
    get_Course_text=session.post(url=url,headers=header,data=data)
    pattern_1 = r'</td><td>(.*?)</td><td>[0-9]'
    pattern_2='<a href="(.*?)"'
    course = re.findall(pattern_1, get_Course_text.text)
    urls=re.findall(pattern_2, get_Course_text.text)
    return dict(zip(course,urls))


def getTeacher_id(course_id):
    teacher_id_list=[]
    teacher_name_list=[]
    url=f"https://jiaowu.cqmu.edu.cn:8080{course_id}"
    teacher_text=session.get(url=url,headers=header)
    pattern_1 = '<a href=\"javascript:void\(0\)\" onclick=\"teacherEvaluate\((.*?), .*?\)\"'
    pattern_2='<a href=\"javascript:void\(0\)\" onclick=\"teacherEvaluate\(.*?, .*?\)\"  title=".*?">(.*?)</a><br>'
    teacher_id = re.findall(pattern_1, teacher_text.text)
    for i in teacher_id:
        if i in teacher_id_list:
            continue
        teacher_id_list.append(i)
    teacher_name=re.findall(pattern_2,teacher_text.text)
    for t in teacher_name:
        if len(t) >3:
            continue
        teacher_name_list.append(t)
    return dict(zip(teacher_id_list,teacher_name_list))

def save_Teacher(id,lesson_id):
    url_ll=f"https://jiaowu.cqmu.edu.cn:8080/eams/evaluateStdByCourseOrTeacher!saveTeacherEvaluate.action?1_326_score=0&1_{id}select326=2&1_327_score=0&1_{id}select327=2&1_324_score=0&1_{id}select324=2&1_325_score=0&1_{id}select325=2&1_322_score=0&1_{id}select322=2&1_323_score=0&1_{id}select323=2&1_321_score=0&1_{id}select321=2&1_330_score=0&1_{id}select330=2&1_331_score=0&1_{id}select331=2&1_328_score=0&1_{id}select328=2&1_329_score=0&1_{id}select329=1&teacherEvaluate.context=&lesson.id={lesson_id}&teacher.id={id}&evalTypeId=1&saveState=2"
    url_sy=f"https://jiaowu.cqmu.edu.cn:8080/eams/evaluateStdByCourseOrTeacher!saveTeacherEvaluate.action?2_343_score=0&2_{id}select343=2&2_342_score=0&2_{id}select342=2&2_341_score=0&2_{id}select341=2&2_351_score=0&2_{id}select351=2&2_350_score=0&2_{id}select350=2&2_349_score=0&2_{id}select349=2&2_348_score=0&2_{id}select348=2&2_347_score=0&2_{id}select347=2&2_346_score=0&2_{id}select346=2&2_345_score=0&2_{id}select345=2&2_344_score=0&2_{id}select344=1&teacherEvaluate.context=&lesson.id={lesson_id}&teacher.id={id}&evalTypeId=2&saveState=2"
    url_sj=f"https://jiaowu.cqmu.edu.cn:8080/eams/evaluateStdByCourseOrTeacher!saveTeacherEvaluate.action?61_76_score=0&61_{id}select76=2&61_129_score=0&61_{id}select129=2&61_128_score=0&61_{id}select128=2&61_127_score=0&61_{id}select127=2&61_364_score=0&61_{id}select364=2&61_126_score=0&61_{id}select126=2&61_365_score=0&61_{id}select365=2&61_125_score=0&61_{id}select125=2&61_122_score=0&61_{id}select122=2&61_363_score=0&61_{id}select363=1&teacherEvaluate.context=&lesson.id={lesson_id}&teacher.id={id}&evalTypeId=61&saveState=2"
    session.get(url=url_ll,headers=header)
    time.sleep(1)
    session.get(url=url_sy,headers=header)
    time.sleep(1)
    session.get(url=url_sj,headers=header)

if __name__ == '__main__':
    course_list=[]
    teacher_list=[]
    print("开始获取课程")
    course_dict=get_Course()
    if get_Course != None:
        print("获取到课程:")
        count=0
        for i in course_dict:
            count+=1
            print(f"{count}.{i}",end="  ")
            course_list.append(i)
    id=int(input("\n选择评教课程(序号):"))
    # print(course_list)
    course_id=course_dict[course_list[id-1]]
    teacher_dict=getTeacher_id(course_id)
    print("获取到教师列表:")
    for i in teacher_dict:
        teacher_list.append(i)
        print(teacher_dict[i],end=" ")

    print("\n开始评教")
    for i in teacher_list:
        print(f"开始评教：{teacher_dict[i]}")
        time.sleep(3)
        save_Teacher(i,course_id[77::])
        print(f"{teacher_dict[i]}评教完成")
    print("评教完成")
