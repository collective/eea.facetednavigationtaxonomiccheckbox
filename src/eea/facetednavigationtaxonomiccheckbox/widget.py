""" 
Taxonomic checkbox widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.utils import DisplayList
from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.dexterity_support import normalize as atdx_normalize
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _
from zope.component import queryUtility
from eea.facetednavigation.interfaces import IFacetedCatalog
from pprint import pprint
from BTrees.IIBTree import weightedIntersection, IISet
import logging
logger = logging.getLogger('eea.facetednavigationtaxonomiccheckbox')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('operator',
        schemata='default',
        required=True,
        vocabulary=DisplayList([('or', 'OR'), ('and', 'AND')]),
        default='or',
        widget=SelectionWidget(
            format='select',
            label=_(u'Default operator'),
            description=_(u'Search with AND/OR between elements'),
            i18n_domain="eea"
        )
    ),
    BooleanField('operator_visible',
        schemata='default',
        required=False,
        default=False,
        widget=BooleanWidget(
            label=_(u"Operator visible"),
            description=_(u"Let the end-user choose to search with "
                          "AND or OR between elements"),
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label=_(u"Vocabulary"),
            description=_(u'Vocabulary to use to render widget items'),
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label=_(u'Catalog'),
            description=_(u"Get unique values from catalog "
                        u"as an alternative for vocabulary"),
        )
    ),
    IntegerField('maxdepth',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_(u"Maximum depth"),
            description=_(u'Number of levels visible of the taxonomy tree'),
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_(u"Reverse options"),
            description=_(u"Sort options reversed"),
        )
    ),
    LinesField('whitelist',
        schemata="display",
        widget=LinesWidget(
            label=_(u'White list tags'),
            description=_(u'Only show specific tags (one per line). Partial tags can be '
                u'entered and are matched if the found tag startswith the partial. Leave empty to show all tags.'),
            i18n_domain="eea"
        )
    ),
    LinesField('default',
        schemata="default",
        widget=LinesWidget(
            label=_(u'Default value'),
            description=_(u'Default items (one per line)'),
            i18n_domain="eea"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'taxonomiccheckbox'
    widget_label = _('Taxonomic checkboxes')
    view_js = '++resource++eea.facetednavigation.widgets.taxonomiccheckbox.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.taxonomiccheckbox.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.taxonomiccheckbox.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.taxonomiccheckbox.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

    def vocabulary(self, **kwargs):
        """ Return data vocabulary
        """
        vocab = super(Widget, self).vocabulary(**kwargs)
        
        nest_vocab = OrderedDict()
        for item in vocab:
            key, value = item
            parts = value.split(".")
            master = nest_vocab
            for index,part in enumerate(parts):
                name = ".".join(parts[:index]+[part,])
                if not name in master:
                  master[name] = OrderedDict()
                  # master[name]['value'] = value
                master = master.get(name)

        return nest_vocab

    def render_partial(self, nested_dict={}, depth=0):
        template = ViewPageTemplateFile('partial.pt')
        return template(self, item=nested_dict, depth=depth)

    def max_depth(self):
        return int(self.data.get('maxdepth', 3) or 3)

    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default
        if not default:
            return []

        if isinstance(default, (str, unicode)):
            default = [default, ]
        return default

    def selected(self, key):
        """ Return True if key in self.default
        """
        if not self.default:
            return False
        for item in self.default:
            if compare(key, item) == 0:
                return True
        return False

    @property
    def operator_visible(self):
        """ Is operator visible for anonymous users
        """
        return self.data.get('operator_visible', False)

    @property
    def operator(self):
        """ Get the default query operator
        """
        return self.data.get('operator', 'and')

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')

        if not self.operator_visible:
            operator = self.operator
        else:
            operator = form.get(self.data.getId() + '-operator', self.operator)

        operator = operator.encode('utf-8', 'replace')

        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        value = atdx_normalize(value)

        if not value:
            return query

        query[index] = {'query': value, 'operator': operator}
        return query

    def taxonomic_label(self, string):
        """
        Taxonomic label.
        """
        return string.split('.')[-1]

    def taxonomic_parent(self, string):
        """
        Taxonomic parent ID.
        """
        return '.'.join(string.split('.')[0:-1])

    def taxonomic_html_class(self, string, depth, repeat):
        """
        Gets taxonomic HTML class.
        """
        class_string = "indent-0"
        if len(string.split('.')) > 1:
            class_string = "indent-1"

        return class_string

    def taxonomic_html_style(self, string):
        style_attrs = [
        ]
        return ';'.join(style_attrs)

    def allowed(self, term):
        allowed = self.data.get('whitelist')

        if term:
            if not allowed:
                return True

            for item in allowed:
                if term.startswith(item):
                    return True


    def _recursive_keys(self, thedict={}, sequence=[]):
        """Since we made nested dicts, we recusrively need to collect keys"""
        for key, item in thedict.items():
            sequence.append(key)
            sequence = self._recursive_keys(item, sequence)

        return sequence


    def count(self, brains, sequence=None):
        """ Intersect results
        """
        res = {}
        sequence = []
        if not sequence:
            sequence = self._recursive_keys(self.vocabulary())

        if not sequence:
            return res

        index_id = self.data.get('index')
        if not index_id:
            return res

        ctool = getToolByName(self.context, 'portal_catalog')
        index = ctool._catalog.getIndex(index_id)
        ctool = queryUtility(IFacetedCatalog)
        if not ctool:
            return res

        brains = IISet(brain.getRID() for brain in brains)
        res[""] = res['all'] = len(brains)
        for value in sequence:
            if not value:
                res[value] = len(brains)
                continue
            normalized_value = atdx_normalize(value)
            rset = ctool.apply_index(self.context, index, normalized_value)[0]
            rset = IISet(rset)
            rset = weightedIntersection(brains, rset)[1]
            if isinstance(value, unicode):
                res[value] = len(rset)
            elif isinstance(normalized_value, unicode):
                res[normalized_value] = len(rset)
            else:
                unicode_value = value.decode('utf-8')
                res[unicode_value] = len(rset)
                
        return res