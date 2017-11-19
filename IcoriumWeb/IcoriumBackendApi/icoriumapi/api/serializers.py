from .models import Quickview
from .models import IcoDetails
from .models import SocialLinks
from .models import SocialArticles
from .models import TeamMembers
from rest_framework import serializers

class QuickviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quickview
        fields = ('IcoId', 'IcoStart', 'IcoEnd', 'Logo', 'CompanyName', 'OneLiner', 'WebsiteUrl', 'Status')

class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ('IcoId', 'Type', 'Link')

class SocialArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialArticles
        fields = ('IcoId', 'Type', 'Title', 'Link')

class TeamMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        fields = ('IcoId', 'Name', 'Position')

class IcoDetailsSerializer(serializers.ModelSerializer):
    SocialArticles = SocialArticlesSerializer(many=True, read_only=True)
    SocialLinks = SocialLinksSerializer(many=True, read_only=True)
    TeamMembers = TeamMembersSerializer(many=True, read_only=True)

    class Meta:
        model = IcoDetails

        fields = ('IcoID', 'IcoSymbol', 'CompanyName', 'OneLiner', 'Logo', 'Description', 'WebsiteUrl', 'Category', 'YearofOrigin', 'CountryofOrigin', 'TechnoDetails', 'UnderlayingTechno', 'AcceptedCurrency', 'IcoPhase', 'IcoStart', 'IcoEnd', 'IcoScale', 'ScaleCurrency', 'IcoTotalExpected', 'TotalCurrency', 'IcoTotalRaised', 'RaisedCurrency', 'TokenDistribution', 'TokenSales', 'InvestmentPotential', 'HypeScore', 'RiskScore', 'OverallRating', 'ExpectedCurrency', 'SocialLinks', 'SocialArticles', 'TeamMembers')
