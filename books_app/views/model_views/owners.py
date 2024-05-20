from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.serializers import serialize
from books_app.models import *
from books_app.forms import *


def owners(request, owner_id):
    # owner_id is the name of an owner
    # Get all owner data for the template
    order_list = ["selected", "", ""]
    if request.method == "POST":
        order_form = OwnerLocationOrderForm(request.POST)
        order = request.POST.get("order")
        order_books = request.POST.get("order_books")
        owner = Owner.objects.get(name=owner_id)
        short_name = owner.name_abbr()
        books = DateOwned.objects.filter(owner=owner).order_by("book_owned__shelfmark")
        relatives = owner.relation.all()
        order_form = OwnerLocationOrderForm()
        library_size = len(books)
        if order == "alphabetical":
            location = owner.owner_location.all().order_by("the_place__name")
            order_list = ["selected", "", ""]
        elif order == "datedesc":
            location = sorted(owner.owner_location.all(), key=lambda a: a.date_range())
            order_list = ["", "selected", ""]
        else:
            location = sorted(owner.owner_location.all(), key=lambda a: a.date_range())
            location.reverse()
            order_list = ["", "", "selected"]

        books_list = []
        for date in books:
            books_list.append([date, date.ownership_type.all()])

        if order_books == "alphabetical":
            order_list = ["selected", "", ""]
        elif order_books == "datedesc":
            books_list = sorted(books_list, key=lambda a: a[0].date_range())
            order_list = ["", "selected", ""]
        elif order_books == "dateasc":
            books_list = sorted(books_list, key=lambda a: a[0].date_range())
            books_list.reverse()
            order_list = ["", "", "selected"]

        books_list_preview = False
        if len(books_list) > 6:
            books_list_preview = books_list[:6]
            books_list = books_list[6:]
        relatives = owner.relation.all()
        up_one = []
        same_gen = []
        down_one = []
        other_rel = []
        down_two = []
        up_two = []
        for relative in relatives:
            if (
                "Spouse" in relative.relation
                or "Brother" in relative.relation
                or "Cousin" in relative.relation
                or "Sister" in relative.relation
            ):
                same_gen.append(relative)
            elif (
                "Grandmother" == relative.relation
                or "Grandfather" == relative.relation
                or "Great Aunt" == relative.relation
                or "Great Uncle" == relative.relation
            ):
                up_two.append(relative)
            elif (
                "Grandson" == relative.relation
                or "Granddaughter" == relative.relation
                or "Grand Niece" == relative.relation
                or "Grand Nephew" == relative.relation
            ):
                down_two.append(relative)
            elif (
                "Father" in relative.relation
                or "Mother" in relative.relation
                or "Aunt" in relative.relation
                or "Uncle" in relative.relation
                or "Parent" in relative.relation
                or "God-parent" in relative.relation
            ):
                up_one.append(relative)
            elif (
                "Son" in relative.relation
                or "Daughter" in relative.relation
                or "son" in relative.relation
                or "daughter" in relative.relation
                or "Niece" in relative.relation
                or "Nephew"
            ):
                down_one.append(relative)
            else:
                other_rel.append(relative)
        # This is a temp fix for issues 74,74,76; Exception Value: local variable 'books_list_preview' referenced before assignment
        # This is a temp fix for issues 74,74,76; Exception Value: local variable 'books_list_preview' referenced before assignment
        if not books_list_preview:
            context = {
                "places": location,
                "relatives": relatives,
                "books": books,
                "order_form": order_form,
                "owner": owner,
                "locations": location,
                "order_list": order_list,
                "library_size": library_size,
                "books_list": books_list,
                "up_one": up_one,
                "down_one": down_one,
                "same_gen": same_gen,
                "other_rel": other_rel,
                "short_name": short_name,
                "down_two": down_two,
                "up_two": up_two,
            }
        else:
            context = {
                "places": location,
                "relatives": relatives,
                "books": books,
                "order_form": order_form,
                "owner": owner,
                "locations": location,
                "order_list": order_list,
                "library_size": library_size,
                "books_list": books_list,
                "up_one": up_one,
                "down_one": down_one,
                "same_gen": same_gen,
                "other_rel": other_rel,
                "books_list_preview": books_list_preview,
                "short_name": short_name,
                "down_two": down_two,
                "up_two": up_two,
            }
        return render(request, "owners.html", context)

    else:
        owner = Owner.objects.get(name=owner_id)
        short_name = owner.name_abbr()
        location = owner.owner_location.all().order_by("-the_place")
        books = DateOwned.objects.filter(owner=owner).order_by("book_owned__shelfmark")
        books_list = []
        for date in books:
            books_list.append([date, date.ownership_type.all()])
        books_list_preview = False
        if len(books_list) > 6:
            books_list_preview = books_list[:6]
            books_list = books_list[6:]
        relatives = owner.relation.all()
        order_form = OwnerLocationOrderForm()
        library_size = len(books)
        up_one = []
        same_gen = []
        down_one = []
        down_two = []
        up_two = []
        other_rel = []
        for relative in relatives:
            if (
                "Spouse" in relative.relation
                or "Brother" in relative.relation
                or "Cousin" in relative.relation
                or "Sister" in relative.relation
            ):
                same_gen.append(relative)
            elif (
                "Grandmother" == relative.relation
                or "Grandfather" == relative.relation
                or "Great Aunt" == relative.relation
                or "Great Uncle" == relative.relation
            ):
                up_two.append(relative)
            elif (
                "Grandson" == relative.relation
                or "Granddaughter" == relative.relation
                or "Grand Niece" == relative.relation
                or "Grand Nephew" == relative.relation
            ):
                down_two.append(relative)
            elif (
                "Father" in relative.relation
                or "Mother" in relative.relation
                or "Aunt" in relative.relation
                or "Uncle" in relative.relation
                or "Parent" in relative.relation
                or "God-parent" in relative.relation
            ):
                up_one.append(relative)
            elif (
                "Son" in relative.relation
                or "Daughter" in relative.relation
                or "son" in relative.relation
                or "daughter" in relative.relation
                or "Niece" in relative.relation
                or "Nephew"
            ):
                down_one.append(relative)
            else:
                other_rel.append(relative)
        # This is a temp fix for issues 74,74,76; Exception Value: local variable 'books_list_preview' referenced before assignment
        if not books_list_preview:
            context = {
                "places": location,
                "relatives": relatives,
                "books": books,
                "order_form": order_form,
                "owner": owner,
                "locations": location,
                "order_list": order_list,
                "library_size": library_size,
                "books_list": books_list,
                "up_one": up_one,
                "down_one": down_one,
                "same_gen": same_gen,
                "other_rel": other_rel,
                "short_name": short_name,
                "down_two": down_two,
                "up_two": up_two,
            }
        else:
            context = {
                "places": location,
                "relatives": relatives,
                "books": books,
                "order_form": order_form,
                "owner": owner,
                "locations": location,
                "order_list": order_list,
                "library_size": library_size,
                "books_list": books_list,
                "up_one": up_one,
                "down_one": down_one,
                "same_gen": same_gen,
                "other_rel": other_rel,
                "books_list_preview": books_list_preview,
                "short_name": short_name,
                "down_two": down_two,
                "up_two": up_two,
            }
        return render(request, "owners.html", context)


def suggest_owner(request):
    if request.method == "POST":
        f = OwnerForm(request.POST)
        if f.is_valid():
            new_article = f.save(commit=False)
            email = request.POST.get("email", "")
            books = request.POST.get("books", "")
            location = request.POST.get("location", "")
            relatives = request.POST.get("relatives", "")

            new_article.comments = (
                "Submitter Contact Info: "
                + email
                + "\nBooks information: "
                + books
                + "\nLocations: "
                + location
                + "\nRelatives: "
                + relatives
            )
            new_article.save()
            return render(request, "suggested.html", {})
        else:
            owner_form = OwnerForm()
            failed = True
            return render(
                request,
                "suggest_owner.html",
                {"owner_form": owner_form, "failed": failed},
            )
    else:
        owner_form = OwnerForm()
        failed = False
        return render(
            request, "suggest_owner.html", {"owner_form": owner_form, "failed": failed}
        )
    

def owners_name_autocomplete(request):
    term = request.GET.get('term', '')
    data = serialize('json', Owner.objects.filter(Q(name__icontains=term) | Q(titles__icontains=term)))
    return HttpResponse(data, content_type='application/json')