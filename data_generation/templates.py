"""
Question templates for different temporal question types
"""

import random

class QuestionTemplates:
    """Templates for generating temporal questions"""
    
    def get_event_attribute_template(self):
        """Get random event attribute template"""
        templates = [
            {
                'question': 'When did {event} occur?',
                'answer_func': lambda e: str(e.get('year', 'Unknown'))
            },
            {
                'question': 'Where did {event} take place?',
                'answer_func': lambda e: e.get('location', 'Unknown')
            },
            {
                'question': 'In which year did {event} happen?',
                'answer_func': lambda e: str(e.get('year', 'Unknown'))
            },
            {
                'question': 'What was the location of {event}?',
                'answer_func': lambda e: e.get('location', 'Unknown')
            }
        ]
        return random.choice(templates)
    
    def get_event_comparison_template(self):
        """Get random event comparison template"""
        templates = [
            {
                'question': 'Which occurred first, {event1} or {event2}?',
                'answer_func': lambda e1, e2: e1['name'] if e1.get('year', 0) < e2.get('year', 0) else e2['name']
            },
            {
                'question': 'Which happened later, {event1} or {event2}?',
                'answer_func': lambda e1, e2: e1['name'] if e1.get('year', 0) > e2.get('year', 0) else e2['name']
            },
            {
                'question': 'Did {event1} happen before {event2}?',
                'answer_func': lambda e1, e2: 'yes' if e1.get('year', 0) < e2.get('year', 0) else 'no'
            }
        ]
        return random.choice(templates)
    
    def get_person_attribute_template(self):
        """Get random person attribute template"""
        templates = [
            {
                'question': 'When was {person} born?',
                'answer_func': lambda p: str(p.get('birth_year', 'Unknown'))
            },
            {
                'question': 'What nationality is {person}?',
                'answer_func': lambda p: p.get('country', 'Unknown')
            },
            {
                'question': 'What field does {person} work in?',
                'answer_func': lambda p: p.get('field', 'Unknown')
            }
        ]
        return random.choice(templates)
    
    def get_counting_template(self):
        """Get random counting template"""
        templates = [
            'How many {domain} events occurred between {start_year} and {end_year}?',
            'What is the count of {domain} events from {start_year} to {end_year}?',
            'How many events in the {domain} domain happened during {start_year}-{end_year}?'
        ]
        return random.choice(templates)
    
    def get_duration_template(self):
        """Get random duration template"""
        templates = [
            'How long did {event} last?',
            'What was the duration of {event}?',
            'For how many years did {event} continue?'
        ]
        return random.choice(templates)
    
    def get_sequence_template(self):
        """Get random sequence template"""
        templates = [
            'What is the chronological order of these events: {events}?',
            'Arrange these events in chronological order: {events}',
            'Order these events from earliest to latest: {events}'
        ]
        return random.choice(templates)
