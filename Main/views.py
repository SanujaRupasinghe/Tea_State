import random

from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta


########################################################################################################################
def FullWorkEmpTable():
    allWorks = Work.objects.all()
    allEmps = Employee.objects.all()

    WorkEmpTable = []
    for rowNo in range(len(allEmps)):
        row = [f'{allEmps[rowNo]}']
        for colNo in range(len(allWorks)):
            work_emp = list(Employee_Work.objects.filter(_work_id=allWorks[colNo].id, _employee_id=allEmps[rowNo].id))
            row.append(None if len(work_emp) == 0 else work_emp[-1].value)
        WorkEmpTable.append(row)

    headerWorkEmpTable = []
    headerWorkEmpTable.extend([work.name for work in allWorks])

    return [headerWorkEmpTable, WorkEmpTable]


def FullWorkSecTable():
    allWorks = Work.objects.all()
    allSections = Section.objects.all()

    WorkSecTable = []
    for rowNo in range(len(allSections)):
        row = [f'{allSections[rowNo]}']
        for colNo in range(len(allWorks)):
            work_sec = list(Section_Work.objects.filter(_work_id=allWorks[colNo].id, _section_id=allSections[rowNo].id))
            row.append(None if len(work_sec) == 0 else work_sec[-1].value)
        WorkSecTable.append(row)

    headerWorkSecTable = []
    headerWorkSecTable.extend([work.name for work in allWorks])

    return [headerWorkSecTable, WorkSecTable]


def WorkEmpDoughnut(work):
    bg = ['rgba(255, 99, 132, 0.4)',
          'rgba(54, 162, 235, 0.4)',
          'rgba(255, 206, 86, 0.4)',
          'rgba(75, 192, 192, 0.4)',
          'rgba(153, 102, 255, 0.4)',
          'rgba(255, 159, 64, 0.4)']
    border = ['rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)']
    if work is None:
        workId = Work.objects.first().id
    else:
        workId = Work.objects.get(name=work).id
    filtered = Employee_Work.objects.filter(_work__id=workId)
    details = [Work.objects.get(id=workId).name, Work.objects.get(id=workId).unit,
               [item._employee.name for item in filtered], [item.value for item in filtered],
               random.sample(bg, len(filtered)), random.sample(border, len(filtered))]
    # ['tea pluck', 'kg', ['saman', 'kamala'], [450.0, 40.0], ['rgba(153, 102, 255, 0.4)', 'rgba(255, 159, 64, 0.4)'], ['rgba(255, 99, 132, 1)', 'rgba(255, 206, 86, 1)']]

    return details


def WorkSectionDoughnut(work):
    bg = ['rgba(255, 99, 132, 0.4)',
          'rgba(54, 162, 235, 0.4)',
          'rgba(255, 206, 86, 0.4)',
          'rgba(75, 192, 192, 0.4)',
          'rgba(153, 102, 255, 0.4)',
          'rgba(255, 159, 64, 0.4)']
    border = ['rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)']
    if work is None:
        workId = Work.objects.first().id
    else:
        workId = Work.objects.get(name=work).id
    filtered = Section_Work.objects.filter(_work__id=workId)
    details = [Work.objects.get(id=workId).name, Work.objects.get(id=workId).unit,
               [item._section.name for item in filtered], [item.value for item in filtered],
               random.sample(bg, len(filtered)), random.sample(border, len(filtered))]
    return details


@login_required
def data(request):
    allWorks = Work.objects.all()
    allSections = Section.objects.all()
    allEmps = Employee.objects.all()

    return render(request, 'Main/data.html',
                  {'allWorks': allWorks, 'allSections': allSections, 'allEmps': allEmps,
                   'FullWorkEmpTable': FullWorkEmpTable(), 'FullWorkSecTable': FullWorkSecTable(),
                   # 'WorkEmpDoughnut': WorkEmpDoughnut(1), 'WorkSecDoughnut': WorkSectionDoughnut(1),
                   'workEmpUrl': '', 'workSectionUrl': '', 'pg_name': 'Data', 'pg_icon': 'blackberry'})


########################################################################################################################
def EmpProgress(start, end, work):
    allEmps = Employee.objects.all()
    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    workId = Work.objects.get(name=work).id

    if (end - start).days < 0:
        end, start = start, end

    details = []
    for i in range(len(allEmps)):
        empId = allEmps[i].id

        want = list(Employee_Work.objects.filter(_employee__id=empId, _work__id=workId))
        wanted = None if len(want) == 0 else int((want[0].value * (end - start).days) / 30)

        now = Entry.objects.filter(employee__id=empId, work__id=workId, date__range=[start, end])
        nowed = None if len(now) == 0 else int(sum([x.amount for x in now]))

        percentage = 0 if wanted is None or nowed is None or wanted == 0 else int((nowed / wanted) * 100)
        details.append([i + 1, list(allEmps)[i].name, nowed, wanted, percentage])

    return details


def SectionProgress(start, end, work):
    allSections = Section.objects.all()
    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    workId = Work.objects.get(name=work).id

    if (end - start).days < 0:
        end, start = start, end

    details = []
    for i in range(len(allSections)):
        sectionId = allSections[i].id

        want = list(Section_Work.objects.filter(_section__id=sectionId, _work__id=workId))
        wanted = None if len(want) == 0 else int((want[0].value * (end - start).days) / 30)

        now = Entry.objects.filter(section__id=sectionId, work__id=workId, date__range=[start, end])
        nowed = None if len(now) == 0 else int(sum([x.amount for x in now]))

        percentage = 0 if wanted is None or nowed is None or wanted == 0 else int((nowed / wanted) * 100)
        details.append([i + 1, list(allSections)[i].name, nowed, wanted, percentage])

    return details


@login_required
def progress(request):
    allWorks = Work.objects.all()
    dates = [datetime(date.today().year, date.today().month, 1).strftime('%Y-%m-%d'),
             (datetime(date.today().year, date.today().month + 1, 1) + timedelta(days=-1)).strftime('%Y-%m-%d')]

    if request.method == 'POST':
        day1 = request.POST.get('day1')
        day2 = request.POST.get('day2')
        work = request.POST.get('works')
        phrase = f'{work} between {day1} and {day2}'
        return render(request, 'Main/progress.html',
                      {'pg_name': 'Progress', 'pg_icon': 'target', 'allWorks': allWorks,
                       'empProgress': EmpProgress(day1, day2, work), 'dates': dates,
                       'sectionProgress': SectionProgress(day1, day2, work),
                       'phrase': phrase})
    else:
        day1 = request.POST.get('day1')
        day2 = request.POST.get('day2')
        work = request.POST.get('works')
        phrase = f'{work} between {day1} and {day2}'
        return render(request, 'Main/progress.html',
                      {'pg_name': 'Progress', 'pg_icon': 'target', 'allWorks': allWorks,
                       'dates': dates, 'phrase': phrase})


########################################################################################################################
@login_required
def maps(request):
    allSections = Section.objects.all()
    return render(request, 'Main/maps.html',
                  {'allSections': allSections, 'pg_name': 'Maps', 'pg_icon': 'google-maps'})


########################################################################################################################
@login_required
def emps(request):
    allEmps = Employee.objects.all()
    return render(request, 'Main/emps.html', {'allEmps': allEmps, 'pg_name': 'Employees', 'pg_icon': 'worker'})


########################################################################################################################
@login_required
def works(request):
    allWorks = Work.objects.all()
    return render(request, 'Main/works.html', {'allWorks': allWorks, 'pg_name': 'Works', 'pg_icon': 'wrench'})


########################################################################################################################
def teaWork(daysLoop, workId):
    TeaWorkList = []
    today = date.today()
    for section in Section.objects.all():
        itemList = list(Entry.objects.filter(section__id=section.id, work__id=workId))
        if len(itemList) != 0:
            delay = (today - itemList[-1].date).days
            if delay >= int(daysLoop):
                TeaWorkList.append([section.name, ((delay-int(daysLoop) + 1)/int(daysLoop))*100, 'bg-danger', itemList[-1].date, 'delay', delay - int(daysLoop)])
            else:
                TeaWorkList.append([section.name, (delay/int(daysLoop))*100, 'bg-primary', itemList[-1].date, 'done', delay])
    return TeaWorkList


def works_details(request, work_id):
    work = Work.objects.get(id=work_id)
    initDaysTeaLoop = 7
    initDaysFertLoop = 70
    if request.method == 'POST':
        daysLoop = request.POST.get('dayLoop')

        if ('Tea' in work.name or 'tea' in work.name) and ('pluck' in work.name or 'Pluck' in work.name):
            return render(request, 'Main/tea_works_details.html',
                          {'work': work, 'pg_name': f'Works | {work.name}', 'pg_icon': 'wrench', 'dayLoop': daysLoop,
                           'TeaWorkList': teaWork(daysLoop, work_id)})
        elif 'fert' in work.name or 'Fert' in work.name:
            return render(request, 'Main/fertilize_works_details.html',
                          {'work': work, 'pg_name': f'Works | {work.name}', 'pg_icon': 'wrench', 'dayLoop': daysLoop,
                           'TeaWorkList': teaWork(daysLoop, work_id)})
        else:
            return render(request, 'Main/under_construction.html',
                          {'work': work, 'pg_name': 'Works', 'pg_icon': 'wrench'})

    else:
        if ('Tea' in work.name or 'tea' in work.name) and ('pluck' in work.name or 'Pluck' in work.name):
            return render(request, 'Main/tea_works_details.html',
                          {'work': work, 'pg_name': f'Works | {work.name}', 'pg_icon': 'wrench',
                           'dayLoop': initDaysTeaLoop, 'TeaWorkList': teaWork(initDaysTeaLoop, work_id)})
        elif 'fert' in work.name or 'Fert' in work.name:
            return render(request, 'Main/fertilize_works_details.html',
                          {'work': work, 'pg_name': f'Works | {work.name}', 'pg_icon': 'wrench',
                           'dayLoop': initDaysFertLoop, 'TeaWorkList': teaWork(initDaysFertLoop, work_id)})
        else:
            return render(request, 'Main/under_construction.html',
                          {'work': work, 'pg_name': 'Works', 'pg_icon': 'wrench'})


########################################################################################################################
@login_required
def calender(request):
    return render(request, 'Main/calender.html', {'pg_name': 'Calender', 'pg_icon': 'calendar'})


########################################################################################################################
def entryFilter(start, end, work, emp):
    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    workId = Work.objects.get(name=work).id
    empId = Employee.objects.get(name=emp).id

    if (end - start).days < 0:
        end, start = start, end
    return Entry.objects.filter(work__id=workId, date__range=[start, end], employee__id=empId)


@login_required
def analysis(request):
    allWorks = Work.objects.all()
    allEmps = Employee.objects.all()
    dates = [datetime(date.today().year, date.today().month, 1).strftime('%Y-%m-%d'),
             (datetime(date.today().year, date.today().month + 1, 1) + timedelta(days=-1)).strftime('%Y-%m-%d')]

    if request.method == 'POST':
        day1 = request.POST.get('day1')
        day2 = request.POST.get('day2')
        work = request.POST.get('works')
        emp = request.POST.get('emps')
        phrase = f'from {emp}, {work} between {day1} and {day2}'
        return render(request, 'Main/analysis.html',
                      {'pg_name': 'Analysis', 'pg_icon': 'table', 'allEntries': entryFilter(day1, day2, work, emp),
                       'allWorks': allWorks, 'allEmps': allEmps, 'dates': dates, 'phrase': phrase})

    else:
        day1 = request.POST.get('day1')
        day2 = request.POST.get('day2')
        work = request.POST.get('works')
        emp = request.POST.get('emps')
        phrase = f'from {emp}, {work} between {day1} and {day2}'
        return render(request, 'Main/analysis.html',
                      {'pg_name': 'Analysis', 'pg_icon': 'table', 'allEntries': Entry.objects.all(),
                       'allWorks': allWorks, 'allEmps': allEmps, 'dates': dates, 'phrase': phrase})


########################################################################################################################
def reminders():
    today = date.today()
    remind = []
    for work in Work.objects.all():
        itemList = list(Entry.objects.filter(work__id=work.id))
        if len(itemList) != 0:
            delay = (today - itemList[-1].date).days
            if delay >= 20:
                remind.append(f'no "{work.name}" done in {delay} days')
    for emp in Employee.objects.all():
        for work in Work.objects.all():
            itemList = list(Entry.objects.filter(employee__id=emp.id, work__id=work.id))
            if len(itemList) != 0:
                delay = (today - itemList[-1].date).days
                if delay >= 20:
                    remind.append(f'"{emp.name}" did not attend in {delay} days for "{work.name}"')
    for section in Section.objects.all():
        for work in Work.objects.all():
            itemList = list(Entry.objects.filter(section__id=section.id, work__id=work.id))
            if len(itemList) != 0:
                delay = (today - itemList[-1].date).days
                if delay >= 20:
                    remind.append(f'"{work.name}" did not done in "{section.name}" section for {delay} days')
    return remind


@login_required
def reminder(request):
    return render(request, 'Main/reminder.html', {'pg_name': 'Reminder', 'pg_icon': 'clock', 'reminders': reminders()})
