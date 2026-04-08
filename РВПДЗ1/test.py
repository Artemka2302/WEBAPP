import subprocess
import pytest

# Для Windows
INTERPRETER = 'python'
# Для MAC
# INTERPRETER = 'python3' 

def run_script(filename, input_data=None):  
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['10', '10'], ['20', '0', '100']),
        (['10000000000', '1'], ['10000000001', '9999999999', '10000000000']),
        (['100', '1'], ['101', '99', '100'])

    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['5', '0'], ['Нет']),
        (['0', '7'], ['0', '0.0'])
    ],
    'loops': [
        ('3', ['0', '1', '4' ]),
        ('6', ['0', '1', '4', '9', '16', '25'])
    ],
    'function' :[
        ('5', '12345'),
        ('14', '1234567891011121314'), 
        ('23', '')
    ],
    'second':[
        (['5', '2', '3', '6', '6', '5'], '5'),
        (['5', '10', '20', '30', '40', '50'], '40'),
        (['6', '100', '90', '100', '80', '100', '70'], '90'),
        (['5', '10', '5', '5', '5', '5'], '5')
    ],
    'nested_list':[
        (['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Харш', '39'], ['Берри', 'Гарри']),
        (['4', 'Иван', '5.0', 'Петр', '4.0', 'Мария', '3.0', 'Анна', '2.0'], ['Петр']),
         (['6', 'Анна', '4.5', 'Борис', '4.5', 'Виктор', '3.0', 'Галина', '3.0', 'Дмитрий', '2.0', 'Елена', '5.0'], ['Анна', 'Борис']),
         (['4', 'Алиса', '4.0', 'Боб', '4.0', 'Чарли', '3.0', 'Дэвид', '4.0'], ['Алиса', 'Боб', 'Дэвид'])
    ],


    'lists': [
        (['12',  'insert 0 5',  'insert 1 10',  'insert 0 6',  'print',  'remove 6',  'append 9',  'append 1',  'sort',  'print',  'pop',  'reverse',  'print'], ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']), 
        (['5', 'append 1', 'append 2', 'append 3', 'print', 'print'], ['[1, 2, 3]', '[1, 2, 3]']),
     
        (['2', 'reverse', 'print'],
     ['[]']),
    ],
    'swap':[
        ('Www.MosPolytech.ru', 'wWW.mOSpOLYTECH.RU'),
        ('Pythonist 2', 'pYTHONIST 2')
    ],
    'split': [
        ('this is a string', 'this-is-a-string'),
        ('I love Informatika in Moscow Polytech', 'I-love-Informatika-in-Moscow-Polytech')
    ],
    'max_word': [
        ('', 'сосредоточенности')
    ],
    'price_sum': [
        ('', '6842.84 5891.06 6810.90')
    ],
    'anagram': [
        (['abc', 'cba'], 'YES'),
        (['hello', 'world'], 'NO'),
        (['listen', 'silent'], 'YES'),
        (['aaa', 'aa'], 'NO'),
        (['123', '321'], 'YES'),
        (['abc', 'abcd'], 'NO')
    ],
    'metro': [
        (['3', '10 20', '15 25', '5 30', '15'], '3'), 
        (['3', '10 20', '15 25', '5 30', '25'], '2'),  
        (['3', '10 20', '15 25', '5 30', '5'], '1'),   
        (['3', '10 20', '15 25', '5 30', '30'], '1'),  
        (['2', '1 5', '6 10', '7'], '1'),              
        (['2', '1 5', '6 10', '11'], '0'),             
        (['1', '1 1', '1'], '1')                        
    ],
    'minion': [
        ('BANANA', 'Стюарт 12'),
        ('A', 'Кевин 1'),
        ('B', 'Стюарт 1'),
        ('AEIOU', 'Кевин 15'),
        
    ],
    'is_leap': [
        ('2000', 'True'),  
        ('2004', 'True'),   
        ('1900', 'False'),  
        ('2100', 'False'),  
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], '1'),
        (['5 3', '1 2 3 4 5', '1 3 5', '2 4'], '1'), 
        (['4 2', '1 1 2 2', '1', '2'], '0'),           
    
    ],
    'pirate': [
        (['10 3', 'золото 5 100', 'серебро 8 120', 'бронза 3 30'], 
        ['золото 5 100', 'серебро 5 75.00']), 
        (['15 4', 'алмазы 3 300', 'золото 5 200', 'серебро 7 210', 'медь 4 80'],
        ['алмазы 3 300', 'золото 5 200', 'серебро 7 210']),  
        (['5 2', 'платина 3 90', 'железо 4 40'],
        ['платина 3 90', 'железо 2 20.00'])  
    ],
    'matrix_mult': [
        (['2', '1 2', '3 4', '5 6', '7 8'], 
        ['19 22', '43 50']), 
        
        (['2', '1 0', '0 1', '2 3', '4 5'],
        ['2 3', '4 5']),  
        
        (['3', '1 2 3', '4 5 6', '7 8 9', '9 8 7', '6 5 4', '3 2 1'],
        ['30 24 18', '84 69 54', '138 114 90']),
        
        (['2', '0 0', '0 0', '1 2', '3 4'],
        ['0 0', '0 0']),  
        
        (['3', '1 0 0', '0 1 0', '0 0 1', '5 5 5', '5 5 5', '5 5 5'],
        ['5 5 5', '5 5 5', '5 5 5']) 
    ]
}

def test_hello_world():
    assert run_script('hello_world.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['function'])
def test_function(input_data, expected):
    assert run_script('print_function.py',[input_data]) == expected 

@pytest.mark.parametrize("input_data, expected", test_data['second'])
def test_second(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_nested(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap'])
def test_swap (input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split'])
def test_split (input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['max_word'])
def test_max_word(input_data, expected):
    assert run_script('max_word.py', []) == expected

@pytest.mark.parametrize("input_data, expected", test_data['price_sum'])
def test_price_sum(input_data, expected):
    assert run_script('price_sum.py', []) == expected

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['minion'])
def test_minion(input_data, expected):
    assert run_script('minion_game.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate'])
def test_pirate(input_data, expected):
    result = run_script('pirate_ship.py', input_data).split('\n')
    assert result == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    result = run_script('matrix_mult.py', input_data).split('\n')
    assert result == expected