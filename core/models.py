from django.db import models

# 1. КАТЕГОРИЯЛАР (Мысалы: Эпитет, Метафора, Кейіпкерлер)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория аты")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"

# 2. АВТОР
class Author(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Автордың аты-жөні")
    gender = models.CharField(max_length=20, choices=[('Er', 'Ер'), ('Ayel', 'Әйел')], verbose_name="Жынысы", null=True, blank=True)
    bio = models.TextField(verbose_name="Өмірдерегі", blank=True)
    main_works = models.TextField(verbose_name="Негізгі еңбектері", blank=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторлар"

# 3. ШЫҒАРМА
class Work(models.Model):
    title = models.CharField(max_length=255, verbose_name="Шығарма аты")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    genre = models.CharField(max_length=100, verbose_name="Жанры", blank=True)
    genre_type = models.CharField(max_length=100, verbose_name="Жанрлық түрі", blank=True)
    style = models.CharField(max_length=100, verbose_name="Стилі", blank=True)
    chronotope = models.CharField(max_length=200, verbose_name="Хронотопы", blank=True)
    theme = models.TextField(verbose_name="Тақырыбы", blank=True)
    abstract = models.TextField(verbose_name="Қысқаша аңдатпа", blank=True)
    created_year = models.CharField(max_length=50, verbose_name="Жазылған жылы", blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Шығарма"
        verbose_name_plural = "Шығармалар"

# 4. КОРПУС ЖАЗБАСЫ (Сөздер мен тіркестер)
class CorpusEntry(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name="Шығарма")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Санаты")
    
    # Негізгі сөз (Мысалы: "Шолақ жұт" немесе "Күшікбай")
    entry_title = models.CharField(max_length=255, verbose_name="Сөз/Тіркес/Кейіпкер аты")
    
    # Түсіндірмесі
    meaning = models.TextField(verbose_name="Мағынасы/Талдауы", blank=True)
    
    # Кітаптан мысал
    example_text = models.TextField(verbose_name="Мәтіндегі қолданысы (Мысал)", blank=True)

    def __str__(self):
        return f"{self.entry_title} ({self.category.name})"

    class Meta:
        verbose_name = "Корпус жазбасы"
        verbose_name_plural = "Корпус жазбалары"

        # ... (Бұрынғы кодтар тұра берсін)

# 5. ОЙЫН: СУРЕТТЕР (3-ші ойын үшін)
class GameImage(models.Model):
    image = models.ImageField(upload_to='game_images/', verbose_name="Сурет")
    correct_answer = models.CharField(max_length=200, verbose_name="Дұрыс жауап (Сөз немесе Шығарма аты)")
    
    def __str__(self):
        return self.correct_answer

    class Meta:
        verbose_name = "Ойын суреті"
        verbose_name_plural = "Ойын суреттері"