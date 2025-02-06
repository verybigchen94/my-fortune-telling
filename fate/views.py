from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, FortuneTellingForm
import random
import requests

def home(request):
    """
    首页视图
    """
    return render(request, 'fate/home.html')

def login_view(request):
    """
    登录视图
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('fortune_telling')
        else:
            return render(request, 'fate/login.html', {'error': '用户名或密码错误'})
    return render(request, 'fate/login.html')

def register_view(request):
    """
    注册视图
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'fate/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'fate/register.html', {'form': form})

@login_required
def logout_view(request):
    """
    退出登录视图
    """
    logout(request)
    return redirect('home')

@login_required
def fortune_telling(request):
    """
    算命视图
    """
    if request.method == 'POST':
        form = FortuneTellingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birth_date = form.cleaned_data['birth_date']
            
            # 生成命理分析
            fortune = generate_fortune(name, birth_date)
            
            return render(request, 'fate/fortune_result.html', {
                'name': name,
                'fortune': fortune
            })
    else:
        form = FortuneTellingForm()
        return render(request, 'fate/fortune_telling.html', {'form': form})


def generate_fortune(name, birth_date):
    """
    调用DeepSeek API生成命理分析
    """
    api_key = 'sk-763883f56e1947bb9dc23807d46fab69'  # 替换为你的API密钥
    api_url = 'https://api.deepseek.com/v1/chat/completions'

    # 构建请求数据
    prompt = f"根据{name}的出生日期{birth_date}，生成一段详细的命理分析，包括性格特点、运势分析和生活建议。"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        fortune_text = result['choices'][0]['message']['content']
        
        return {
            'fortune_text': fortune_text
        }
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return {
            'fortune_text': "算命失败，请稍后再试。"
        }