# This software and any associated files are copyright 2010 Brian Carver and
# Michael Lissner.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Under Sections 7(a) and 7(b) of version 3 of the GNU Affero General Public
#  License, that license is supplemented by the following terms:
#
#  a) You are required to preserve this legal notice and all author
#  attributions in this program and its accompanying documentation.
#
#  b) You are prohibited from misrepresenting the origin of any material
#  within this covered work and you are required to mark in reasonable
#  ways how any modified versions differ from the original version.


import sys
sys.path.append('/var/www/court-listener/alert')

import settings
from django.core.management import setup_environ
setup_environ(settings)

from search.models import Document
from alert.lib.db_tools import queryset_generator
from optparse import OptionParser

# adding alert to the front of this breaks celery. Ignore pylint error.
from scrapers.tasks import extract_doc_content

def fixer(simulate=False, verbose=False):
    '''OCR documents that lack content'''
    #docs = queryset_generator(Document.objects.filter(source='C', documentPlainText=''))
    docs = Document.objects.raw('''select "documentUUID" 
                                   from "Document"
                                   where "source" = 'C' and  
                                       "documentPlainText" = 'Unable to extract document content.'
                                    ''')
    for doc in docs:
        if verbose:
            print "Fixing document number %s: %s" % (doc.pk, doc)

        if not simulate:
            # Extract the contents asynchronously.
            extract_doc_content.delay(doc.pk)

def main():
    usage = "usage: %prog [--verbose] [---simulate]"
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', action="store_true", dest='verbose',
        default=False, help="Display log during execution")
    parser.add_option('-s', '--simulate', action="store_true",
        dest='simulate', default=False, help=("Simulate the corrections without "
        "actually making them."))
    (options, args) = parser.parse_args()

    verbose = options.verbose
    simulate = options.simulate

    if simulate:
        print "*******************************************"
        print "* SIMULATE MODE - NO CHANGES WILL BE MADE *"
        print "*******************************************"

    return fixer(simulate, verbose)
    exit(0)

if __name__ == '__main__':
    main()
