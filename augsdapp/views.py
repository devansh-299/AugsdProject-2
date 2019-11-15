from django.shortcuts import render, redirect
from .forms import AddCourseForm,AddSectionForm
from .models import SecClass,Room,Course
from django.contrib import messages
from django.db.models import Q

def homepage(request):
    return render(request, 'augsdapp/homepage.html', {})

def AddCourse(request):
	if request.method =="POST":
		form = AddCourseForm(request.POST)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('AddSection')
	else:
		form = AddCourseForm()
	return render(request, 'augsdapp/AddCourse.html', {'form':form})

def AddSection(request):
	if request.method=="POST":
		form = AddSectionForm(request.POST)
		if form.is_valid():
			instructorCheck = SecClass.objects.filter(startTime__gte=form.cleaned_data.get('startTime'),
				endTime__lte=form.cleaned_data.get('endTime'),
				days=form.cleaned_data.get('days')).count()
			classSize = form.cleaned_data.get('classSize')
			roomSelected = form.cleaned_data.get('room')
			if instructorCheck != 0:
				messages.success(request, 'Instructor not available for the selected time slot')
				form = AddSectionForm(request.POST)
			elif classSize > roomSelected.capacity:
				messages.success(request, 'Room cannot accomodate more participants')
				form = AddSectionForm(request.POST)
			else:
				post=form.save(commit=False)
				post.save()
				messages.success(request, 'Successful')
				return redirect('AddCourse') 
	else:
		form=AddSectionForm()
	return render(request,'augsdapp/AddSection.html',{'form':form})

def ModifyCourse(request):
	if request.method=="GET":
		search_query = request.GET.get('q',None)
		submitbutton= request.GET.get('submit')
		if search_query is not None:
			lookups = Q(courseCode__icontains=search_query)
			results = Course.objects.filter(lookups).distinct()

			context={'results': results,
			'submitbutton': submitbutton}
			return render(request, 'augsdapp/ModifyCourse.html', context)
		else:
			messages.success(request, 'No Course Found')
			return render(request, 'augsdapp/ModifyCourse.html')
	else:
		return render(request, 'augsdapp/ModifyCourse.html')

def DeleteCourse(request):
	return render(request, 'augsdapp/DeleteCourse.html', {})

# Implementing search for Modify/Delete

