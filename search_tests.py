from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']

        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)


    #  keyword_to_title test. 

    def test_keyword_to_titles_case_sensitive(self):
        keyword_dict = [
            ['List of Canadian musicians', 'author1', 3567876543, 97547, ['c', 'd', 'H']],
            ['2009 in music', 'author2', 5876543267, 4564, ['d', 'h']], 
            ['Lights (musician)', 'author3', 8655459, 14678, ['c', 'h']], 
            ['Will Johnson (soccer)', 'author4', 51267897, 75325, ['d', 'l']]
        ]
        expected = {
            'c': ['List of Canadian musicians','Lights (musician)'],
            'd': ['List of Canadian musicians', '2009 in music', 'Will Johnson (soccer)'], 
            'H': ['List of Canadian musicians'], 
            'h': ['2009 in music', 'Lights (musician)'],
            'l': ['Will Johnson (soccer)'],
                } 
        
        self.assertEqual(keyword_to_titles(keyword_dict), expected)

    def test_keyword_to_titles_empty_input(self):
        # Test with an empty dictionary
        keyword_dict = []
        expected = {}
        
        self.assertEqual(keyword_to_titles(keyword_dict), expected)

    
    def test_keyword_to_titles_case_sensitive_unique_title(self):
        
        keyword_dict = [
            ['List of Canadian musicians', 'author1', 3567876543, 97547, ['c']],
            ['2009 in music', 'author2', 5876543267, 4564, ['d']], 
            ['Lights (musician)', 'author3', 8655459, 14678, ['h']], 
            ['Will Johnson (soccer)', 'author4', 51267897, 75325, ['l']]
        ]
        expected = {
        'c': ['List of Canadian musicians'],
        'd': ['2009 in music',], 
        'h': ['Lights (musician)'],
        'l': ['Will Johnson (soccer)'],
                } 
       
        self.assertEqual(keyword_to_titles(keyword_dict), expected)


    # title_to_info test

    def test_title_to_info(self):
        keyword = [
            ['S', 't', 'v', 'e'],
            ['W', 'i', 'l', 'l']
        ]
        
        expected = {'S': {'author': 't',  'timestamp' : 'v' , 'length': 'e'},
         'W': {'author': 'i', 'timestamp' : 'l', 'length': 'l'}}
        
        self.assertEqual (title_to_info(keyword), expected)

    def test_title_to_info_empty(self):
        keyword = []
        expected = {}
        
        self.assertEqual(title_to_info(keyword), expected)

    def  test_title_to_info_case_sensitivity(self):
        keyword = [
            ['S', 't', 'v', 'e'],
            ['W', 'i', 'l', 'l'],
            ['w', 'I', 'L', 'L']
        ]
        
        expected = {'S': {'author': 't',  'timestamp' : 'v' , 'length': 'e'},
         'W': {'author': 'i', 'timestamp' : 'l', 'length': 'l'},
         'w': {'author': 'I', 'timestamp' : 'L', 'length': 'L'}}
        
        self.assertEqual (title_to_info(keyword), expected)


    # search test

    def test_search_case_sensitive(self):
        keyword = 'canadian'
        keyword_to_titles = { 'canadian' : ['List of Canadian musicians', '2009 in music', 'Lights (musician)', 'Will Johnson (soccer)', '2007 in music', '2008 in music']}
        expected = ['List of Canadian musicians', '2009 in music', 'Lights (musician)', 'Will Johnson (soccer)',  '2007 in music', '2008 in music']
        
        self.assertEqual(search(keyword, keyword_to_titles), expected)

    def test_search_empty(self):
        keyword = ""
        keyword_to_titles = {}
        expected = []

        self.assertEqual(search(keyword, keyword_to_titles), expected)

    def test_search_beach(self):
        keyword = 'beach'
        keyword_to_titles = {'beach':  ['Spain national beach soccer team']}
        expected =  ['Spain national beach soccer team']

        self.assertEqual(search(keyword, keyword_to_titles), expected)

    def test_search_no_matching_keyword(self):
        keyword = 'sports'
        keyword_to_titles = {'music': ['List of Canadian musicians', '2009 in music', 'Lights (musician)', 'Will Johnson (soccer)', '2007 in music', '2008 in music']}
        expected = []

        self.assertEqual(search(keyword, keyword_to_titles), expected)


    # article_length test

    def test_article_length_all_titles(self):
        # All titles should be returned
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'Joe', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected  = ['music city', 'ran', 'kim']

        self.assertEqual(article_length(6000, article_titles, titles_to_info), expected)


    def test_article_length_empty(self):
        # empty 
        titles_to_info = {}
        article_titles = []
        expected  = []

        self.assertEqual(article_length(7000, article_titles, titles_to_info), expected)

    def test_article_length_zero(self):
        # zero length
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'Joe', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected  = []

        self.assertEqual(article_length(0, article_titles, titles_to_info), expected)

    def test_article_length_no_fit(self):
        # no title found

        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'Joe', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected  = []

        self.assertEqual(article_length(50, article_titles, titles_to_info), expected)


    # key_by_author

    def test_key_by_author_empty_input(self):
        # Test with empty lists for article_titles
        article_titles = []
        title_to_info = {}
        expected = {}

        self.assertEqual(key_by_author(article_titles, title_to_info), expected)

    def test_key_by_author(self):
        # Test with lists for article_titles
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'Mary', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected = {
            'Mary' : ['music city', 'ran'],
            'Andrea' : ['kim']
        }    

        self.assertEqual(key_by_author(article_titles, titles_to_info), expected)

    def test_key_by_author_empty_title(self):
        # Test with empty lists for article_titles
        titles_to_info = {}
        article_titles = []
        expected = {}

        self.assertEqual(key_by_author(article_titles, titles_to_info), expected)
    
    def test_key_by_author_case_sensitive(self):
        # Test with lists for article_titles, case sensitive
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'MARY', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected = {
            'Mary' : ['music city'],
            'MARY' : ['ran'],
            'Andrea' : ['kim']
        }

        self.assertEqual(key_by_author(article_titles, titles_to_info), expected)
    

    # filter_to_author
    
    def test_filter_to_author_empty_input(self):
        # Test with an empty list for article_titles
        author_name = 'jack johnson'
        article_titles = []
        title_to_info = {}
        expected = []

        self.assertEqual(filter_to_author(author_name, article_titles, title_to_info), expected)

    def test_filter_to_author(self):
        # Test with an empty list for article_titles
        author_name = 'Mary'
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'MARY', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']
        expected = ['music city']

        self.assertEqual(filter_to_author(author_name, article_titles, titles_to_info), expected)
    
    def test_filter_to_author_wrong_author(self):
        # Test with an list for article_titles with wrong author
        author_name = 'Oyinade'
        titles_to_info = {
            'music city': {"author": 'Mary', "timestamp":2005, "length": 300},
            'ran': {"author": 'MARY', "timestamp": 1988, "length": 5000},
            'kim': {"author": 'Andrea', "timestamp": 1960, "length": 200}
            }
        article_titles = ['music city', 'ran', 'kim']          
        expected = []
    
        self.assertEqual(filter_to_author(author_name, article_titles, titles_to_info), expected)


    # filter_out

    def test_filter_out_empty_keyword_and_article_titles(self):
        keyword = 'music'
        article_titles = []
        keyword_to_titles = {'music' : []}
        expected = []

        self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected)

    def test_filter_out_empty_keyword(self):
        # Test with empty article_titles and keyword_to_titles
        keyword = ''
        keyword_to_titles  = {}
        article_titles = []
        expected = []

        self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected)

    def test_filter_out_case_sensitive(self):
        keyword = 'Music'
        article_titles = ['say', 'city', 'ran']
        keyword_to_titles = {'music': ['city', 'ran']}
        expected = ['say', 'city', 'ran']

        self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected)

    def test_filter_out_special_characters(self):
        keyword = '$#@!'
        article_titles = ['say', 'city', 'ran']
        keyword_to_titles = {'$#@!': ['city', 'ran']}
        expected = ['say']

        self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected)


    # article_from_year test.

    def test_articles_from_year_basic(self):
        year = 2008
        article_titles = ['say', 'city', 'ran']
        title_to_info = {'say': {'timestamp': 1199145600}, 'city': {'timestamp': 1220251200}, 'ran': {'timestamp': 1230768000}}
        expected = ['say', 'city']

        self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected)

    def test_articles_from_year_no_matching_year(self):
        year = 2010
        article_titles = ['say', 'city', 'ran']
        title_to_info = {'say': {'timestamp': 1199145600}, 'city': {'timestamp': 1220251200}, 'ran': {'timestamp': 1230768000}}
        expected = []

        self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected)

    def test_articles_from_year_empty_article_titles(self):
        year = 2008
        article_titles = []
        title_to_info = {'say': {'timestamp': 1199145600}, 'city': {'timestamp': 1220251200}, 'ran': {'timestamp': 1230768000}}
        expected = []

        self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected)

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_integration_test(self, input_mock):
        keyword = 'beach'
        advanced_option = 1
        advanced_response = 7000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team']\n"

        self.assertEqual(output, expected)


    @patch('builtins.input')
    def test_key_by_author_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2
        
        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_to_author_integration_test(self, input_mock):
        keyword = 'music'
        advanced_option = 3
        advanced_response = 'jack johnson'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Noise (music)', '1986 in music', 'Tim Arnold (musician)', 'David Gray (musician)', 'Alex Turner (musician)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_out_keyword_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'music'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_search_integration_test(self, input_mock):
        keyword = 'radio'
        advanced_option = 6
        

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['List of Canadian musicians', 'French pop music', '1922 in music', 'Rock music', 'Steve Perry (musician)']\n"

        self.assertEqual(output, expected)


    

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
