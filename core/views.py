from django.shortcuts import render, redirect
from .models import Author, Work, Category, CorpusEntry, GameImage # GameImage моделі бар деп есептейміз
from django.db.models import Q
import random
import json

# --- БАСТЫ БЕТТЕР ---


def index(request):
    query = request.GET.get('q')
    author_id = request.GET.get('author')
    work_id = request.GET.get('work')
    category_ids = request.GET.getlist('category')

    results = CorpusEntry.objects.all()

    if query:
        results = results.filter(entry_title__icontains=query)
    if author_id and author_id != 'all':
        results = results.filter(work__author_id=author_id)
    if work_id and work_id != 'all':
        results = results.filter(work_id=work_id)
    if category_ids:
        results = results.filter(category_id__in=category_ids)

    # Егер ешқандай фильтр болмаса, бос қайтару (немесе қаласаңыз барлығын)
    if not any([query, author_id != 'all', work_id != 'all', category_ids]):
        results = CorpusEntry.objects.none()

    context = {
        'results': results,
        'authors': Author.objects.all(),
        'works': Work.objects.all(),
        'categories': Category.objects.all(),
        'selected_categories': category_ids,
        'query': query
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def games_home(request):
    return render(request, 'games_home.html')

# --- 1. ТЕСТ ОЙЫНЫ (QUIZ) ---
def game_quiz(request):
    # 1. НӘТИЖЕ ЖІБЕРІЛСЕ (POST) - Нәтиже бетін көрсетеміз
    if request.method == 'POST':
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith('q_'):
                user_answers[key.split('_')[1]] = value 
        
        results = []
        correct_count = 0
        total_questions = len(user_answers)
        
        entry_ids = user_answers.keys()
        entries = CorpusEntry.objects.filter(id__in=entry_ids)
        
        for entry in entries:
            user_answer = user_answers.get(str(entry.id))
            is_correct = (entry.meaning.strip().lower() == user_answer.strip().lower())
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'id': entry.id,
                'question': entry.entry_title,
                'correct_answer': entry.meaning,
                'user_answer': user_answer,
                'is_correct': is_correct,
            })
            
        half_score = total_questions / 2

        context = {
            'results': results,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'half_score': half_score
        }
        return render(request, 'game_quiz_results.html', context)

    # 2. ОЙЫНДЫ БАСТАУ (GET with params) - Ойнау бетін көрсетеміз
    if request.GET.get('start_game'):
        work_id = request.GET.get('work')
        count = int(request.GET.get('count', 5))
        
        # Сөзі мен мағынасы бар жазбаларды ғана аламыз
        entries = CorpusEntry.objects.filter(meaning__isnull=False).exclude(meaning__exact='')
        
        # Егер нақты шығарма таңдалса, сүзгіден өткіземіз
        if work_id and work_id != 'all':
            entries = entries.filter(work_id=work_id)
        
        entries = list(entries)
        
        # Егер сұрақ саны жеткіліксіз болса, барлығын аламыз
        if len(entries) < count:
            count = len(entries)
            
        random.shuffle(entries)
        selected_entries = entries[:count]
        
        quiz_data = []
        all_meanings = [e.meaning for e in CorpusEntry.objects.all() if e.meaning]

        for item in selected_entries:
            # 3 қате жауап (distractors) таңдау
            distractors = random.sample(all_meanings, 3) if len(all_meanings) >= 3 else all_meanings[:3]
            options = list(set(distractors + [item.meaning]))
            random.shuffle(options)
            
            quiz_data.append({
                'id': item.id,
                'question': item.entry_title,
                'options': options,
                'correct_answer': item.meaning
            })
        
        # Егер сұрақтар табылмаса, ескерту жасауға болады (қазірше бос тізім кетеді)
        return render(request, 'game_quiz_play.html', {'quiz_data': quiz_data})

    # 3. БАПТАУ БЕТІ (Default GET) - Таңдау бетін көрсетеміз
    works = Work.objects.all()
    return render(request, 'game_quiz_setup.html', {'works': works})
# --- 2. СӘЙКЕСТЕНДІРУ ОЙЫНЫ (MATCH) ---
def game_match(request):
    # НӘТИЖЕ (POST)
    if request.method == 'POST':
        results_json = request.POST.get('match_results', '[]')
        user_matches = json.loads(results_json)
        
        results = []
        correct_count = 0
        total_questions = len(user_matches)

        for match in user_matches:
            entry_id = match['id']
            user_match_id = match['matched_id']
            
            # Сөз бен Мағынаның ID-лері сәйкес келе ме?
            is_correct = (int(entry_id) == int(user_match_id))
            
            if is_correct:
                correct_count += 1
            
            try:
                entry = CorpusEntry.objects.get(id=entry_id)
                results.append({
                    'question': entry.entry_title,
                    'correct_meaning': entry.meaning,
                    'is_correct': is_correct,
                })
            except CorpusEntry.DoesNotExist:
                continue
            
        half_score = total_questions / 2
        context = {
            'results': results,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'half_score': half_score
        }
        return render(request, 'game_match_results.html', context)
        
    # ОЙЫН (GET)
    count = int(request.GET.get('count', 5))
    entries = list(CorpusEntry.objects.filter(meaning__isnull=False).exclude(meaning__exact='')[:20])
    random.shuffle(entries)
    selected = entries[:count]
    
    words = [{'id': x.id, 'text': x.entry_title} for x in selected]
    meanings = [{'id': x.id, 'text': x.meaning} for x in selected]
    random.shuffle(meanings)
    
    return render(request, 'game_match_play.html', {'words': words, 'meanings': meanings, 'count': count})

# --- 3. СУРЕТТІ ТАП (PICTURE) ---
def game_picture(request):
    # Бұл ойынды кейінірек толықтырамыз, әзірге бос шаблон
    return render(request, 'games_home.html')