KEY_TAG = 'tag'
KEY_ATTRIBUTE = 'attribute'
POSSIBLE_FONTS = {
    'https://medium.com' : {
        KEY_TAG : 'article',
        KEY_ATTRIBUTE : {}
    },
    'https://codare.aurelio.net' : {
        KEY_TAG : 'div',
        KEY_ATTRIBUTE : {'class':'entry-content'}
    },
    'https://www.digitalocean.com' : {
        KEY_TAG : 'div',
        KEY_ATTRIBUTE : {'class':'content-body tutorial-content'}
    },
    'https://www.clubedohardware.com.br' : {
        KEY_TAG : 'div',
        KEY_ATTRIBUTE : {'id':'comments'}
    },
    'https://academiahopper.com.br' : {
        KEY_TAG : 'div',
        KEY_ATTRIBUTE : {'id':'primary', 'class':'content-area primary'}
    },
    'https://pt.stackoverflow.com' : {
        KEY_TAG : 'div',
        KEY_ATTRIBUTE : {'id':'mainbar', 'role':'main', 'aria-label':'pergunta e respostas'}
    }

}

TOKENT_TEXT_SEPARATOR = '<->'

SEARCH_KEYWORD = 'google search'
DEFAULT_BROWSER_BOOTING_VALUE = False
DEFAULT_AVAILABLE_STATUS = False

FIRST_ACCESS_TIMEOUT = 3
