from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с формой"""
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    """Обработка формы и расчет площади"""
    area = None
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            length = float(request.form.get('length', 0))
            width = float(request.form.get('width', 0))
            
            # Рассчитываем площадь
            area = length * width
        except ValueError:
            area = "Ошибка: введите числовые значения"
    
    return render_template('index.html', area=area)

if __name__ == '__main__':
    app.run(debug=True)