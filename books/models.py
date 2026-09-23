from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.




class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        max_length=170,
        unique=True
    )

    biography = models.TextField(
        blank=True
    )

    photo = models.ImageField(
        upload_to="authors/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=255,
        unique=True
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books"
    )

    description = models.TextField()

    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True
    )

    # Physical and digital pricing
    physical_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0)
        ]
    )

    digital_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0)
        ]
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    # Recommended reading age
    age_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(18)
        ]
    )

    age_max = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(18)
        ]
    )

    publisher = models.CharField(
        max_length=200,
        blank=True
    )

    pages = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    language = models.CharField(
        max_length=50,
        default="English"
    )

    # Book poster
    poster = models.ImageField(
        upload_to="books/posters/",
        blank=True,
        null=True
    )

    poster_url = models.URLField(
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["category", "is_active"]
            ),
            models.Index(
                fields=["is_featured", "is_active"]
            ),
        ]

    def clean(self):
        super().clean()

        # A book must have at least one format.
        if (
            self.physical_price is None
            and self.digital_price is None
        ):
            raise ValidationError(
                "A book must have a physical price, "
                "a digital price, or both."
            )

        # Poster must be either an uploaded image or a URL.
        if self.poster and self.poster_url:
            raise ValidationError(
                "A book poster must be either an uploaded image "
                "or a poster URL, not both."
            )

        # Validate age range.
        if (
            self.age_min is not None
            and self.age_max is not None
            and self.age_min > self.age_max
        ):
            raise ValidationError(
                "Minimum age cannot be greater than maximum age."
            )

    @property
    def available_format(self):
        """
        Determines the available book format
        from the prices.
        """

        if (
            self.physical_price is not None
            and self.digital_price is not None
        ):
            return "BOTH"

        if self.physical_price is not None:
            return "PHYSICAL"

        if self.digital_price is not None:
            return "DIGITAL"

        return None

    @property
    def poster_source(self):
        """
        Returns the available poster source.
        """

        if self.poster:
            return self.poster.url

        if self.poster_url:
            return self.poster_url

        return None

    def __str__(self):
        return self.title


class BookSpecification(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="specifications"
    )

    name = models.CharField(
        max_length=100
    )

    value = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.book.title} - {self.name}"


class DigitalBook(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name="digital_content"
    )

    file = models.FileField(
        upload_to="books/digital/"
    )

    file_type = models.CharField(
        max_length=20,
        default="PDF"
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        super().clean()

        if (
            self.book
            and self.book.digital_price is None
        ):
            raise ValidationError(
                "A digital book must have a digital price."
            )

    def __str__(self):
        return f"Digital: {self.book.title}"