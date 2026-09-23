from django.contrib import admin

# Register your models here.


from .models import (
    Author,
    Book,
    BookSpecification,
    Category,
    DigitalBook,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "image_status",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Category Image",
            {
                "description": (
                    "Provide either an uploaded image or an image URL. "
                    "Do not provide both."
                ),
                "fields": (
                    "image",
                    "image_url",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Image")
    def image_status(self, obj):
        if obj.image:
            return "Uploaded image"

        if obj.image_url:
            return "Image URL"

        return "No image"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "biography",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "available_format_display",
        "physical_price",
        "digital_price",
        "stock",
        "is_featured",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "isbn",
        "author__name",
        "category__name",
    )

    list_filter = (
        "category",
        "author",
        "is_featured",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "available_format_display",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "author",
                    "category",
                    "description",
                    "isbn",
                )
            },
        ),
        (
            "Pricing & Availability",
            {
                "fields": (
                    "physical_price",
                    "digital_price",
                    "stock",
                    "available_format_display",
                )
            },
        ),
        (
            "Book Information",
            {
                "fields": (
                    "age_min",
                    "age_max",
                    "publisher",
                    "pages",
                    "language",
                )
            },
        ),
        (
            "Book Poster",
            {
                "fields": (
                    "poster",
                    "poster_url",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def available_format_display(self, obj):
        return obj.available_format

    available_format_display.short_description = "Format"


@admin.register(BookSpecification)
class BookSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "name",
        "value",
    )

    search_fields = (
        "book__title",
        "name",
        "value",
    )

    list_filter = (
        "name",
    )


@admin.register(DigitalBook)
class DigitalBookAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "file_type",
        "is_available",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "book__title",
    )

    list_filter = (
        "file_type",
        "is_available",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )