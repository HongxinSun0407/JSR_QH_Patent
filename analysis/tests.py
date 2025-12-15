import json
import re
from itertools import zip_longest

from django.conf import settings
from django.test import TestCase
from openai.types import file_content

from analysis.views import request_moonshot_ai

# Create your tests here.

