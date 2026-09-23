from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book, Category
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    featured_books = (
        Book.objects
        .filter(
            is_active=True,
            is_featured=True
        )
        .select_related("author", "category")[:8]
    )

    categories = Category.objects.filter(
        is_active=True
    )

    context = {
        "featured_books": featured_books,
        "categories": categories,
    }

    return render(
        request,
        "storefront/home.html",
        context
    )

def book_list(request):
    books = (
        Book.objects
        .filter(is_active=True)
        .select_related("author", "category")
    )

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    book_format = request.GET.get("format", "").strip().upper()

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(isbn__icontains=query)
        )

    if category_slug:
        books = books.filter(
            category__slug=category_slug
        )

    if book_format == "PHYSICAL":
        books = books.filter(
            physical_price__isnull=False
        )

    elif book_format == "DIGITAL":
        books = books.filter(
            digital_price__isnull=False
        )

    sort = request.GET.get("sort", "newest").strip()

    if sort == "oldest":
        books = books.order_by("created_at")

    elif sort == "title_asc":
        books = books.order_by("title")

    elif sort == "title_desc":
        books = books.order_by("-title")

    elif sort == "price_low":
        books = books.order_by("physical_price", "digital_price")

    elif sort == "price_high":
        books = books.order_by(
            "-physical_price",
            "-digital_price"
        )

    else:
        books = books.order_by("-created_at")

    paginator = Paginator(books, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)


    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "categories": Category.objects.filter(
            is_active=True
        ),
        "query": query,
        "selected_category": category_slug,
        "selected_format": book_format,
        "selected_sort": sort,
        "breadcrumb_current": "Books",
    }

    return render(
        request,
        "storefront/books.html",
        context,
    )

def book_detail(request, slug):
    book = get_object_or_404(
        Book.objects
        .select_related("author", "category")
        .prefetch_related("specifications"),
        slug=slug,
        is_active=True,
    )

    context = {
        "book": book,
        "specifications": book.specifications.all(),
        "breadcrumb_books": True,
        "breadcrumb_current": book.title,
    }

    return render(
        request,
        "storefront/book_detail.html",
        context,
    )


def category_books(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True,
    )

    books = (
        Book.objects
        .filter(
            category=category,
            is_active=True,
        )
        .select_related("author", "category")
    )

    context = {
        "category": category,
        "books": books,
        "breadcrumb_categories": True,
        "breadcrumb_current": category.name,
    }

    return render(
        request,
        "storefront/category.html",
        context,
    )

def book_search(request):
    query = request.GET.get("q", "").strip()

    books = Book.objects.filter(
        is_active=True
    ).select_related(
        "author",
        "category",
    )

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(isbn__icontains=query)
        )

    context = {
        "books": books,
        "query": query,
    }

    return render(
        request,
        "storefront/search.html",
        context,
    )

def category_list(request):
    categories = (
        Category.objects
        .filter(is_active=True)
        .order_by("name")
    )

    context = {
        "categories": categories,
        "breadcrumb_categories": True,
    }

    return render(
        request,
        "storefront/categories.html",
        context,
    )