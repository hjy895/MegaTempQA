"""
Historical knowledge base for temporal questions
"""

class KnowledgeBase:
    """Curated historical knowledge for QA generation"""
    
    def __init__(self):
        self.events = []
        self.people = []
        self.organizations = []
    
    def load(self):
        """Load all knowledge base data"""
        print("🧠 Loading knowledge base...")
        self._load_events()
        self._load_people()
        self._load_organizations()
        print(f"✅ Loaded: {len(self.events)} events, {len(self.people)} people, {len(self.organizations)} orgs")
    
    def get_stats(self):
        """Get knowledge base statistics"""
        return {
            'events': len(self.events),
            'people': len(self.people),
            'organizations': len(self.organizations)
        }
    
    def _load_events(self):
        """Load historical events"""
        events_data = [
            # Major Wars
            {'name': 'World War I', 'year': 1914, 'end_year': 1918, 'location': 'Europe', 'casualties': 17000000, 'domain': 'military'},
            {'name': 'World War II', 'year': 1939, 'end_year': 1945, 'location': 'Global', 'casualties': 75000000, 'domain': 'military'},
            {'name': 'Korean War', 'year': 1950, 'end_year': 1953, 'location': 'Korea', 'casualties': 3000000, 'domain': 'military'},
            {'name': 'Vietnam War', 'year': 1955, 'end_year': 1975, 'location': 'Vietnam', 'casualties': 3800000, 'domain': 'military'},
            
            # Space Events
            {'name': 'Sputnik Launch', 'year': 1957, 'location': 'Soviet Union', 'casualties': 0, 'domain': 'science'},
            {'name': 'Moon Landing', 'year': 1969, 'location': 'United States', 'casualties': 0, 'domain': 'science'},
            {'name': 'First Human in Space', 'year': 1961, 'location': 'Soviet Union', 'casualties': 0, 'domain': 'science'},
            
            # Natural Disasters
            {'name': '2004 Indian Ocean Tsunami', 'year': 2004, 'location': 'Indian Ocean', 'casualties': 280000, 'domain': 'disaster'},
            {'name': 'Hurricane Katrina', 'year': 2005, 'location': 'United States', 'casualties': 1800, 'domain': 'disaster'},
            {'name': 'Haiti Earthquake', 'year': 2010, 'location': 'Haiti', 'casualties': 316000, 'domain': 'disaster'},
            
            # Modern Events
            {'name': 'September 11 Attacks', 'year': 2001, 'location': 'United States', 'casualties': 3000, 'domain': 'terrorism'},
            {'name': 'COVID-19 Pandemic', 'year': 2020, 'location': 'Global', 'casualties': 7000000, 'domain': 'health'},
            {'name': 'Arab Spring', 'year': 2011, 'location': 'Middle East', 'casualties': 100000, 'domain': 'politics'},
            
            # Technology
            {'name': 'Internet Creation', 'year': 1989, 'location': 'Global', 'casualties': 0, 'domain': 'technology'},
            {'name': 'iPhone Launch', 'year': 2007, 'location': 'United States', 'casualties': 0, 'domain': 'technology'},
            {'name': 'Facebook Launch', 'year': 2004, 'location': 'United States', 'casualties': 0, 'domain': 'technology'},
        ]
        
        for i, event_data in enumerate(events_data):
            event = {
                'id': f"EVENT_{i}",
                'name': event_data['name'],
                'year': event_data['year'],
                'end_year': event_data.get('end_year', event_data['year']),
                'location': event_data['location'],
                'casualties': event_data['casualties'],
                'domain': event_data['domain'],
                'source': 'curated'
            }
            self.events.append(event)
    
    def _load_people(self):
        """Load notable people"""
        people_data = [
            # Scientists
            {'name': 'Albert Einstein', 'birth': 1879, 'death': 1955, 'country': 'Germany', 'field': 'Physics'},
            {'name': 'Marie Curie', 'birth': 1867, 'death': 1934, 'country': 'Poland', 'field': 'Chemistry'},
            {'name': 'Stephen Hawking', 'birth': 1942, 'death': 2018, 'country': 'United Kingdom', 'field': 'Physics'},
            
            # Politicians
            {'name': 'Winston Churchill', 'birth': 1874, 'death': 1965, 'country': 'United Kingdom', 'field': 'Politics'},
            {'name': 'Nelson Mandela', 'birth': 1918, 'death': 2013, 'country': 'South Africa', 'field': 'Politics'},
            {'name': 'John F. Kennedy', 'birth': 1917, 'death': 1963, 'country': 'United States', 'field': 'Politics'},
            
            # Technology
            {'name': 'Steve Jobs', 'birth': 1955, 'death': 2011, 'country': 'United States', 'field': 'Technology'},
            {'name': 'Bill Gates', 'birth': 1955, 'death': None, 'country': 'United States', 'field': 'Technology'},
            {'name': 'Elon Musk', 'birth': 1971, 'death': None, 'country': 'United States', 'field': 'Technology'},
        ]
        
        for i, person_data in enumerate(people_data):
            person = {
                'id': f"PERSON_{i}",
                'name': person_data['name'],
                'birth_year': person_data['birth'],
                'death_year': person_data['death'],
                'country': person_data['country'],
                'field': person_data['field'],
                'source': 'curated'
            }
            self.people.append(person)
    
    def _load_organizations(self):
        """Load organizations"""
        orgs_data = [
            {'name': 'United Nations', 'founded': 1945, 'country': 'International', 'type': 'International Organization'},
            {'name': 'NASA', 'founded': 1958, 'country': 'United States', 'type': 'Space Agency'},
            {'name': 'Apple Inc.', 'founded': 1976, 'country': 'United States', 'type': 'Technology Company'},
            {'name': 'Microsoft Corporation', 'founded': 1975, 'country': 'United States', 'type': 'Technology Company'},
            {'name': 'Google', 'founded': 1998, 'country': 'United States', 'type': 'Technology Company'},
        ]
        
        for i, org_data in enumerate(orgs_data):
            org = {
                'id': f"ORG_{i}",
                'name': org_data['name'],
                'inception_year': org_data['founded'],
                'country': org_data['country'],
                'type': org_data['type'],
                'source': 'curated'
            }
            self.organizations.append(org)
