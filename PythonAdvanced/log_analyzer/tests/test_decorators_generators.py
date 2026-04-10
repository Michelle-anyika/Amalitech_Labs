import pytest
from src.utils.decorators import timer_decorator, cache_decorator, log_call
from src.utils.generators import read_large_log, group_logs_by_status

def test_timer_decorator(capsys):
    @timer_decorator
    def sample_func():
        return "Done"
    
    result = sample_func()
    assert result == "Done"
    captured = capsys.readouterr()
    assert "Execution time" in captured.out
    
def test_cache_decorator():
    calls = 0
    
    @cache_decorator
    def expensive_op(x):
        nonlocal calls
        calls += 1
        return x * 2
        
    assert expensive_op(5) == 10
    assert calls == 1
    assert expensive_op(5) == 10  # Called from LRU cache
    assert calls == 1 

def test_log_call_decorator(capsys):
    @log_call
    def say_hi(name):
        return f"Hi {name}"
        
    say_hi("Alice")
    captured = capsys.readouterr()
    assert "Calling function 'say_hi' with args: ('Alice',)" in captured.out

def test_read_large_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("Line 1\nLine 2\nLine 3")
    
    # Must yield generators, NOT arrays!
    gen = read_large_log(log_file)
    assert next(gen).strip() == "Line 1"
    assert next(gen).strip() == "Line 2"

def test_groupby_status():
    dicts = [
        {'status': '200', 'bytes': '10'},
        {'status': '200', 'bytes': '20'},
        {'status': '404', 'bytes': '30'}
    ]
    groups = group_logs_by_status(dicts)
    assert '200' in groups
    assert '404' in groups
    assert len(groups['200']) == 2
