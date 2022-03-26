from dal import autocomplete
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import *

# Create your views here.
# Disclaimer: this doesn't seem efficient but this version runs the fastest
def index(request):
    texts_about = len(Text.objects.all())
    owners_about = len(Owner.objects.filter(gender="Female"))
    books_about = len(Book.objects.filter(reviewed=True))
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            # Get form data
            display = request.POST.getlist("display")
            query = request.POST.get("search", "")
            author = request.POST.get("author", "")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            tag = request.POST.get("genre", "")
            text = request.POST.get("text", "")
            language = request.POST.get("language", "")
            shelfmark = request.POST.get("shelfmark", "")
            owners_search = request.POST.get("owner", "")

            # Get books matching shelfmark search, all books if blank
            books_objs = Book.objects.filter(shelfmark__icontains=shelfmark)

            # Author Search Field
            author_result = Author.objects.filter(name__icontains=author)
            texts_from_author = []
            books_from_author = []
            # For all the authors in a search result, add the texts which correspond to them
            if len(author) == 0:
                texts_from_author = Text.objects.all()
            else:
                for t in Text.objects.all():
                    if set(author_result) & set(t.authors.all()):
                        texts_from_author.append(t)

            # Find all books in which each text appears
            for text_obj in texts_from_author:
                book = Book.objects.filter(text=text_obj)
                for b in book:
                    books_from_author.append(b)
            # Modifies books_objs to be only the elements that appear in both lists
            if len(author) != 0:
                books_objs = set(books_from_author) & set(books_objs)

            # Text Search Field- abbreviated version of author process
            texts_from_text = list(
                set(Text.objects.filter(title__icontains=text))
                | set(Text.objects.filter(name_eng__icontains=text))
            )
            books_from_text = []
            for item in texts_from_text:
                book = Book.objects.filter(text=item)
                for c in book:
                    books_from_text.append(c)
            if len(text) != 0:
                books_objs = set(books_from_text) & set(books_objs)

            # Language Search Field - find all books in which text in specific language appears
            if len(language) !=0:
                texts_from_language = []
                books_from_language = []
                language_result = BooksLanguage.objects.filter(language__icontains=books_language)
                for a in Text.objects.all():
                    if set(language_result) & set(a.laguages.all()):
                        texts_from_language.append(a)

                for text_obj_language in texts_from_language:
                    book = Book.obects.filter(text=text_obj_language)
                    for c in book:
                        books_from_language.append(c)
                books_objs = set(books_from_language) & set(books_objs)
            else:
                texts_from_language = Text.objects.all()       
            
            # Tag Search Field- same as author, but tags are ManyToManyField
            if len(tag) != 0:
                texts_from_tag = []
                books_from_tag = []
                tag_result = Tag.objects.filter(tag__icontains=tag)
                for a in Text.objects.all():
                    if set(tag_result) & set(a.tags.all()):
                        texts_from_tag.append(a)

                for text_obj_tag in texts_from_tag:
                    book = Book.objects.filter(text=text_obj_tag)
                    for c in book:
                        books_from_tag.append(c)
                books_objs = set(books_from_tag) & set(books_objs)
            # For the purpose of populating the search results
            else:
                texts_from_tag = Text.objects.all()

            # BookLocations for every book- we need a list of locations to map and date filter
            z = []
            books_to_filter = []
            for book in books_objs:
                z.append(book.book_location.all().order_by("date"))
            # z is a list of querysets, so we need to unpack
            for locs in z:
                for loc in locs:
                    books_to_filter.append(loc)

            # Owner Search Field
            owners_objs = Owner.objects.filter(name__icontains=owners_search)

            books_from_owners = []
            for owners_obj in owners_objs:
                books_from_owners.append(
                    BookLocation.objects.filter(owner_at_time=owners_obj)
                )
            books_from_owners1 = []
            for query in books_from_owners:
                for lst in query:
                    books_from_owners1.append(lst)
            books_to_filter = list(set(books_from_owners1) & set(books_to_filter))
            # Per profs. request- if user searches for texts the owners which owned those texts must appear
            # on the map as well
            owners_from_books = []
            # If we got any query about texts/books
            if (
                len(shelfmark) != 0
                or len(text) != 0
                or len(author) != 0
                or len(tag) != 0
            ):
                # For every book we find the dates of ownership
                for book_obj in books_objs:
                    date_for_owner = DateOwned.objects.filter(book_owned=book_obj)
                    for owner_date in date_for_owner:
                        owners_from_books.append(owner_date.book_owner)
                # Compare the owners from their independent search and the owners from the book search- get duplicates
                owners_objs = set(owners_from_books) & set(owners_objs)

            # OwnerPlaceDateLived for each owner- we need a list of locations to map and date filter
            t = []
            owner_to_filter = []
            for owner in owners_objs:
                t.append(owner.owner_location.all().order_by("date_at_location"))
            for queryset in t:
                for item in queryset:
                    owner_to_filter.append(item)

            # Display options
            if len(display) == 0 or (display[0] == "owners" and len(display) != 2):
                # If we only want to display owners
                books_to_filter = []
            if len(display) == 1 and display[0] == "books":
                # If we only want to display books
                owner_to_filter = []

            # Get a date range- a list of a start date and end date in datetime format
            searchRange = []
            # Check for non-year formatting, i.e. if not len(4) and if any numbers are in string
            if len(start_date) != 4 or any(char.isalpha() for char in start_date):
                # Default date otherwise
                searchRange.append(datetime.datetime(1350, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(start_date), 1, 1))
            if len(end_date) != 4 or any(char.isalpha() for char in end_date):
                searchRange.append(datetime.datetime(1500, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(end_date), 1, 1))

            # Date range search field- filtered by BookLocation and OwnerPlaceDateLived objects
            books_final = []
            for date in books_to_filter:
                dateRange = date.date_range()
                # decide to display each book or not by comparing list of datetimes for overlap
                if not (dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    books_final.append(date)

            # Same process for each OwnerPlaceDateLived
            owners_final = []
            for owner_date in owner_to_filter:
                dateRange = owner_date.date_range()
                if not (dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    owners_final.append(owner_date)

            # Helps display search results by reverse querying
            owners_search = []
            for owner_location in owners_final:
                toAppend = Owner.objects.get(owner_location=owner_location)
                owners_search.append(toAppend)
            # Get rid of duplicates
            owners_search = list(set(owners_search))
            owner_len = len(owners_search)
            owners_search_preview = []
            if owner_len > 5:
                owners_search_preview = owners_search[:5]
                owners_search = owners_search[5:]

            books_search = []
            for book_location in books_final:
                toAdd = Book.objects.get(book_location=book_location)
                books_search.append(toAdd)
            books_search = list(set(books_search))
            book_len = len(books_search)
            books_search_preview = []
            if book_len > 5:
                books_search_preview = books_search[:5]
                books_search = books_search[5:]

            # For displaying information about the search
            texts_from_books = []
            q = []
            for v in books_search:
                q.append(v.text.all())
            for textquery in q:
                for listing in textquery:
                    texts_from_books.append(listing)
            texts_search = list(
                set(texts_from_text) & set(texts_from_tag) & set(texts_from_author)
            )
            if not (author or tag or text):
                texts_search = list(set(texts_search).union(set(texts_from_books)))
            if not (books_search or owners_search) and not (author or text or tag):
                texts_search = []
            texts_search_preview = []
            text_len = len(texts_search)
            if text_len > 5:
                texts_search_preview = texts_search[:5]
                texts_search = texts_search[5:]
            display_search = True

            return render(
                request,
                "index.html",
                {
                    "books_search": books_search,
                    "owners_search": owners_search,
                    "search_form": search_form,
                    "owners": owners_final,
                    "display": display,
                    "books": books_final,
                    "book_len": book_len,
                    "owner_len": owner_len,
                    "text_len": text_len,
                    "texts_search": texts_search,
                    "books_search_preview": books_search_preview,
                    "owners_search_preview": owners_search_preview,
                    "texts_search_preview": texts_search_preview,
                    "display_search": display_search,
                    "books_about": books_about,
                    "owners_about": owners_about,
                    "texts_about": texts_about,
                },
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        # Default display is all female owners
        books = []
        locations = Location.objects.all()
        authors = Author.objects.all()
        owners = Owner.objects.filter(gender="Female")
        owners_default = []
        for owner in owners:
            toAdd = owner.owner_location.all()
            for item in toAdd:
                owners_default.append(item)
        search_form = SearchForm()
        display_search = False

        return render(
            request,
            "index.html",
            {
                "books": books,
                "locations": locations,
                "search_form": search_form,
                "authors": authors,
                "owners": owners_default,
                "display_search": display_search,
                "books_about": books_about,
                "owners_about": owners_about,
                "texts_about": texts_about,
            },
        )


def books(request, book_id):
    # book_id comes from the url- is a book's shelfmark
    # Get all the data we need on a book and send to template
    book = Book.objects.get(shelfmark=book_id)
    texts = book.text.all()
    bibs = book.bibliography.all()
    # Geo data for the template map
    places = BookLocation.objects.filter(book_shelfmark=book)
    illuminators = book.illuminators.all()
    scribes = book.scribes.all()
    printers = book.printer.all()
    # For owners we query DateOwned objects because they contain dates which we need to be on template
    # orders by date_range method... i think
    owners_date = sorted(
        DateOwned.objects.filter(book_owned=book), key=lambda a: a.date_range()
    )
    date_list = []
    for date in owners_date:
        date_list.append([date, date.ownership_type.all()])
    # owners_date = DateOwned.objects.filter(book_owned=book).order_by('dateowned')
    owner_geo = []
    evidences = []
    for date in owners_date:
        try:
            # In case some misc dateowned objects appear- if everything has a link and we clean up this isn't necessary
            owner_geo.append(date)
            evidences.append([date, date.ownership_type.all()])
        except:
            pass
    return render(
        request,
        "books.html",
        {
            "book": book,
            "owners": owner_geo,
            "texts": texts,
            "bibs": bibs,
            "places": places,
            "iluminators": illuminators,
            "scribes": scribes,
            "printers": printers,
            "evidences": evidences,
            "date_list": date_list,
        },
    )


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


def texts(request, text_id):
    # text_id is the title of a text
    text = Text.objects.get(title=text_id)
    books = Book.objects.filter(text=text)
    languages = text.language.all()
    authors = text.authors.all()
    translators = text.translators.all()
    tags = text.tags.all()
    places = []
    dates = []
    # Geo data for the map
    for book in books:
        locations = book.book_location.all()
        for location in locations:
            # For every book the text is in add the locations of that book
            places.append(location)
        toAdd = book.owner_info.all()
        for date in toAdd:
            # Add DateOwned objects to a list for display
            dates.append(date)
    books_list = []
    for date in dates:
        books_list.append([date, date.ownership_type.all()])
    return render(
        request,
        "texts.html",
        {
            "text": text,
            "books": books,
            "languages": languages,
            "tags": tags,
            "places": places,
            "dates": dates,
            "authors": authors,
            "translators": translators,
            "books_list": books_list,
        },
    )


def loadup(request):
    # Inactive- used for database loading
    return HttpResponse("Success")


def search(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
    else:
        search_form = SearchForm()
        dates = DateOwned.objects.all()
        owners = Owner.objects.all()
        books = Book.objects.all()
        texts = Text.objects.all()

    return render(
        request,
        "search.html",
        {
            "search_form": search_form,
            "dates": dates,
            "owners": owners,
            "books": books,
            "texts": texts,
        },
    )


def teach(request):
    return render(request, "teach.html")


# Inactive- to be used for autocomplete
class BooksAutocomplete(autocomplete.Select2ListView):
    def create(self, text):  # To create a new object
        return text

    def get_list(self):
        list = [book.shelfmark for book in Book.objects.all()]

        if self.q:
            filter_result = Book.objects.all().filter(shelfmark__icontains=self.q)
            list = [book.shelfmark for book in filter_result]
        return list


def about(request):
    about = About.objects.all()
    about = [about[0], about[1], about[2], about[3]]
    return render(request, "about.html", {"about": about})


def suggest_sel(request):
    return render(request, "suggest_sel.html", {})


def suggest_book(request):
    if request.method == "POST":
        f = BookForm(request.POST)
        if f.is_valid():
            new_article = f.save(commit=False)
            text = request.POST.get("text", "")
            email = request.POST.get("email", "")
            scribes = request.POST.get("scribes", "")
            illuminators = request.POST.get("illuminators", "")
            printer = request.POST.get("printer", "")
            book_location = request.POST.get("book_location", "")
            owner_info = request.POST.get("owner_info", "")
            bibliography = request.POST.get("bibliography", "")

            new_article.comments = (
                "Submitter Contact Info: "
                + email
                + "\nText: "
                + text
                + "\nIlluminators: "
                + illuminators
                + "\nScribes: "
                + scribes
                + "\n"
            )
            new_article.comments += (
                "Printers: "
                + printer
                + "\nBook Locations: "
                + book_location
                + "\nOwner Info"
                + owner_info
                + "\n"
            )
            new_article.comments += "Bibliography: : " + bibliography + "\n"
            new_article.save()
            text = request.POST.get("text", "")
            return render(request, "suggested.html", {})
        else:
            book_form = BookForm()
            failed = True
            return render(
                request, "suggest_book.html", {"book_form": book_form, "failed": failed}
            )
    else:
        book_form = BookForm()
        failed = False
        return render(
            request, "suggest_book.html", {"book_form": book_form, "failed": failed}
        )


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


def bibliography(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
    else:
        search_form = SearchForm()
        bibs = Bibliography.objects.all().values('source', 'author_date').distinct()
    return render(
        request, "bibliography.html", {"search_form": search_form, "bibs": bibs}
    )
