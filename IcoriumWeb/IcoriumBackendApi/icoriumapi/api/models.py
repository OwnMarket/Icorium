from django.db import models

class Quickview(models.Model):
    IcoId = models.CharField(max_length=10, default='', primary_key=True)
    IcoStart = models.DateTimeField(null=True)
    IcoEnd = models.DateTimeField(null=True)
    CompanyName = models.CharField(max_length=200, null=True)
    OneLiner = models.CharField(max_length=500, null=True)
    WebsiteUrl = models.CharField(max_length=200, null=True)
    Logo = models.CharField(max_length=200, null=True)
    Status = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'Quickview'


class IcoDetails(models.Model):
    IcoID = models.CharField(max_length=10, default='', primary_key=True)
    IcoSymbol = models.CharField(max_length=20, null=True)
    CompanyName = models.CharField(max_length=200, null=True)
    OneLiner = models.CharField(max_length=200, null=True)
    Logo = models.CharField(max_length=200, null=True)
    Description = models.CharField(max_length=4000, null=True)
    WebsiteUrl = models.CharField(max_length=200, null=True)
    Category = models.CharField(max_length=200, null=True)
    YearofOrigin = models.CharField(max_length=4, null=True)
    CountryofOrigin = models.CharField(max_length=200, null=True)
    TechnoDetails = models.CharField(max_length=200, null=True)
    UnderlayingTechno = models.CharField(max_length=200, null=True)
    AcceptedCurrency = models.CharField(max_length=200, null=True)
    IcoPhase = models.CharField(max_length=200, null=True)
    IcoStart = models.DateTimeField(null=True) 
    IcoEnd = models.DateTimeField(null=True)
    IcoScale = models.CharField(max_length=200, null=True)
    ScaleCurrency = models.CharField(max_length=200, null=True)
    IcoTotalExpected = models.CharField(max_length=200, null=True)
    TotalCurrency = models.CharField(max_length=200, null=True)
    IcoTotalRaised = models.CharField(max_length=200, null=True)
    RaisedCurrency = models.CharField(max_length=200, null=True)
    TokenDistribution = models.CharField(max_length=200, null=True)
    TokenSales = models.CharField(max_length=200, null=True)
    InvestmentPotential = models.CharField(max_length=200, null=True)
    HypeScore = models.CharField(max_length=200, null=True)
    RiskScore = models.CharField(max_length=200, null=True)
    OverallRating = models.CharField(max_length=200, null=True)
    ExpectedCurrency = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'IcoMaster'

class SocialLinks(models.Model):
    LinkID = models.CharField(max_length=10, default='', primary_key=True)
    IcoId = models.CharField(max_length=10, null=True)
    Type = models.CharField(max_length=20, null=True)
    Link = models.CharField(max_length=200, null=True)
    IcoDetails = models.ForeignKey(IcoDetails, related_name="SocialLinks", db_column="IcoId") 

    class Meta:
        db_table = 'SocialLinks'
        unique_together = (('Type', 'Link'),)

class SocialArticles(models.Model):
    ArticleID = models.CharField(max_length=10, default='', primary_key=True)
    IcoId = models.CharField(max_length=10, null=True)
    Type = models.CharField(max_length=20, null=True)
    Title = models.CharField(max_length=1000, null=True)
    Link = models.CharField(max_length=200, null=True)
    IcoDetails = models.ForeignKey(IcoDetails, related_name="SocialArticles", db_column="IcoId") 

    class Meta:
        db_table = 'SocialArticles'
        unique_together = (('Type', 'Link'),)

class TeamMembers(models.Model):
    TeamMemberID = models.CharField(max_length=10, default='', primary_key=True)
    IcoId = models.CharField(max_length=10, null=True)
    Name = models.CharField(max_length=200, null=True)
    Position = models.CharField(max_length=200, null=True)
    IcoDetails = models.ForeignKey(IcoDetails, related_name="TeamMembers", db_column="IcoId") 

    class Meta:
        db_table = 'TeamMember'
        unique_together = (('Name', 'Position'),)
