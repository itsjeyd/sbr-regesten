""" This module defines the data model of the Sbr Regesten webapp. """

from django.db import models


class Regest(models.Model):
    """
    The Regest model represents a single regest.
    """

    title = models.CharField(max_length=70)
    location = models.CharField(max_length=70, null=True)
    regest_type = models.CharField(max_length=70, null=True)
    content = models.TextField()

    issuer = models.OneToOneField("Person", null=True)
    mentions = models.ManyToManyField("Concept", null=True)

    original_date = models.TextField(null=True)
    seal_info = models.TextField()
    print_info = models.TextField()
    translation_info = models.TextField(null=True)
    original_info = models.TextField()
    xml_repr = models.TextField()

    def __unicode__(self):
        return u'Regest {0}: {1}'.format(self.id, self.title)


class Archive(models.Model):
    """
    The Archive model represents information about a specific archive
    associated with one or more regests.

    TODO: Add examples
    """

    regest = models.ForeignKey("Regest")
    info = models.TextField()

    def __unicode__(self):
        return u'{0}'.format(self.content)


class RegestDate(models.Model):
    """
    The RegestDate model represents the date of a single regest.

    TODO: Add examples
    """

    OFFSET_TYPES = (
        ('vor', 'vor'),
        ('nach', 'nach'),
        ('um', 'um'),
        ('ca.', 'ca.'),
        ('kurz nach', 'kurz nach'),)

    regest = models.OneToOneField("Regest")
    start = models.DateField()
    start_offset = models.CharField(
        max_length=20, choices=OFFSET_TYPES, null=True)
    end = models.DateField()
    end_offset = models.CharField(
        max_length=20, choices=OFFSET_TYPES, null=True)
    alt_date = models.DateField(null=True)

    @property
    def exact(self):
        return not self.start_offset and not self.end_offset

    def __unicode__(self):
        return u'\nStarts on {0}\nEnds on {1}\n\n---> ({2})'.format(
            self.start, self.end, 'exact' if self.exact else 'not exact')


class Footnote(models.Model):
    """
    The footnote model represents footnotes referenced e.g. in the
    content of a regest.
    """

    regest = models.ForeignKey("Regest")
    content = models.TextField()

    def __unicode__(self):
        return u'Footnote {0}:\n{1}'.format(self.id, self.content)


class Concept(models.Model):
    """
    The Concept model groups attributes common to all types of
    IndexEntries.
    """

    name = models.TextField()
    additional_names = models.TextField(null=True)
    related_concepts = models.ManyToManyField("self", null=True)

    def __unicode__(self):
        return u'Concept {0}: {1}'.format(self.id, self.name)


class Landmark(Concept):
    """
    The landmark model represents a single landmark listed or
    mentioned in the index of the Sbr Regesten.
    """

    landmark_type = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        landmark =  u'Landmark {0}: {1}'.format(self.id, self.name)
        if self.landmark_type:
            landmark += u' [{0}]'.format(self.landmark_type)
        return landmark


class Location(Concept):
    """
    The Location model represents a single location listed or
    mentioned in the index of the Sbr Regesten.
    """

    location_type = models.CharField(max_length=30, null=True)
    w = models.NullBooleanField()
    w_ref = models.CharField(max_length=100, null=True)
    reference_point = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=70, null=True)
    region = models.ForeignKey("Region", null=True)
    country = models.ForeignKey("Country", null=True)

    def __unicode__(self):
        location = u'Location {0}: {1}'.format(self.id, self.name)
        if self.location_type:
            location += u' [{0}]'.format(self.location_type)
        return location


class Person(Concept):
    """
    The Person model represents a single individual listed or
    mentioned in the index of the Sbr Regesten.
    """

    forename = models.CharField(max_length=70, null=True)
    surname = models.CharField(max_length=70, null=True)
    genname = models.CharField(max_length=30, null=True)
    maidenname = models.CharField(max_length=70, null=True)
    info = models.TextField(null=True)
    profession = models.CharField(max_length=30, null=True)
    resident_of = models.ForeignKey("Location", null=True)

    def __unicode__(self):
        return u'Person {0}: {1}'.format(self.id, self.name)


class PersonGroup(Concept):
    """
    The PersonGroup model represents a single group of people related
    e.g. by their profession.
    """

    members = models.ManyToManyField("Person")

    def __unicode__(self):
        return u'PersonGroup {0}: {1}'.format(self.id, self.name)


class Family(PersonGroup):
    """
    The family model represents a single family.
    """

    location = models.ForeignKey("Location", null=True)

    def __unicode__(self):
        return u'Family {0}: {1}'.format(self.id, self.name)

    class Meta:
        """
        Specifies metadata and options for the Family model.
        """

        verbose_name_plural = "families"


class IndexEntry(models.Model):
    """
    The IndexEntry model represents a single entry in the index of the
    Sbr Regesten.
    """

    defines = models.OneToOneField("Concept")
    related_entries = models.OneToOneField("self", null=True)
    xml_repr = models.TextField()

    def __unicode__(self):
        return u'IndexEntry {0}\n\n{1}'.format(self.id, self.defines)

    class Meta:
        """
        Specifies metadata and options for the IndexEntry model.
        """

        verbose_name_plural = "index entries"


class Region(models.Model):
    """
    The Region model represents regions mentioned in the (index of
    the) Sbr Regesten.
    """

    REGION_TYPES = (
        ('Bundesland', 'Bundesland'),
        ('Departement', 'Departement'),
        ('Provinz', 'Provinz'))

    name = models.CharField(max_length=70)
    region_type = models.CharField(max_length=30, choices=REGION_TYPES)

    def __unicode__(self):
        return u'{0}: ({1})'.format(self.name, self.region_type)


class Country(models.Model):
    """
    The Country model represents countries mentioned in the (index of
    the) Sbr Regesten.
    """

    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    class Meta:
        """
        Specifies metadata and options for the Country model.
        """

        verbose_name_plural = "countries"
