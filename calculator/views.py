# views.py
from django.http import JsonResponse
from django.views import View
import requests
from collections import deque
import time

WINDOW_SIZE = 10

API_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

class NumberWindow:
    def __init__(self, size):
        self.size = size
        self.window = deque()

    def add_numbers(self, numbers):
        for n in numbers:
            if n not in self.window:
                self.window.append(n)
                if len(self.window) > self.size:
                    self.window.popleft()

    def average(self):
        return sum(self.window) / len(self.window) if self.window else 0

window_no = NumberWindow(WINDOW_SIZE)

class ViewNum(View):
    def get(self, request, numberid):
        if numberid not in API_URLS:
            return JsonResponse({'error': 'Invalid number ID'}, status=400)

        url = API_URLS[numberid]

        access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE3ODI2NTEzLCJpYXQiOjE3MTc4MjYyMTMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImIzN2I0MmY1LWFlMDMtNGY0NC1iOTFiLTY1YjJkMjc1N2YwOSIsInN1YiI6IjIxMzExQTA1TDdAc3JlZW5pZGhpLmVkdS5pbiJ9LCJjb21wYW55TmFtZSI6IlNyZWVuaWRoaSBJbnN0aXR1dGUgT2YgU2NpZW5jZSBhbmQgVGVjaG5vbG9neSIsImNsaWVudElEIjoiYjM3YjQyZjUtYWUwMy00ZjQ0LWI5MWItNjViMmQyNzU3ZjA5IiwiY2xpZW50U2VjcmV0IjoidWdKdkVUUXRid2lSQWRXQyIsIm93bmVyTmFtZSI6IkFudmVzaCBOYWdvdGh1Iiwib3duZXJFbWFpbCI6IjIxMzExQTA1TDdAc3JlZW5pZGhpLmVkdS5pbiIsInJvbGxObyI6IjIxMzExQTA1TDcifQ.dnV1S6_cduSCJpCStDUFZOLePW1We4j-KHazLzIcbo8"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=0.5)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.5:
                raise requests.exceptions.Timeout()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Failed to get numbers from the server: {str(e)}'}, status=500)

        numbers = data.get('numbers', [])
        previous = list(window_no.window)
        window_no.add_numbers(numbers)
        current = list(window_no.window)
        average = window_no.average()

        return JsonResponse({
            'numbers': numbers,
            'windowPrevState': previous,
            'windowCurrState': current,
            'avg': average
        })
