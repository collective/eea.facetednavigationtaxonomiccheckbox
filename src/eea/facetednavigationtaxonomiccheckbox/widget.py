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

from eea.facetednavigation.dexterity_support import normalize as atdx_normalize
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


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
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_(u"Maximum items"),
            description=_(u'Number of items visible in widget'),
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_(u"Reverse options"),
            description=_(u"Sort options reversed"),
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

    def taxonomic_html_class(self, string):
        """
        Gets taxonomic HTML class.
        """
        return "indent-{0}".format(len(string.split('.')) - 1)

    def taxonomic_html_style(self, string):
        factor = 20
        indent = len(string.split('.')) - 1
        style_attrs = [
            'margin-left: {0}px'.format(indent * factor)
        ]
        return ';'.join(style_attrs)
