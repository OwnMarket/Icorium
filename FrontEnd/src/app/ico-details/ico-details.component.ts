import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { IcoApiService } from '../ico-api.service';

@Component({
  selector: 'app-ico-details',
  templateUrl: './ico-details.component.html',
  styleUrls: ['./ico-details.component.css']
})
export class IcoDetailsComponent implements OnInit {
  icoApiService: IcoApiService;
  activatedRoute: ActivatedRoute;
  icoDetails;
  icoSubscription;
  today = new Date();
  icoStart;
  icoEnd;
  icoPhase = 'no data available';
  icoRaised;
  icoExpected;
  icoScale;
  icoRaisedCurrency;
  icoExpectedCurrency;
  icoScaleCurrency;
  icoArticle = false;
  icoFacebook = false;
  icoTwitter = false;
  icoTeam = false;

  constructor(activatedRoute: ActivatedRoute, icoApiService: IcoApiService) {
    this.activatedRoute = activatedRoute;
    this.icoApiService = icoApiService;
  }

  ngOnInit() {
    this.activatedRoute.params.subscribe(
      params => {
        this.icoApiService.setIcoId(params['id'])
        this.icoApiService.fetchIcoDetails();
        this.icoDetails = this.icoApiService.getIcoDetails();
      }
    );
    this.icoSubscription = this.icoApiService.viewIcoDetails.subscribe(
      () => {
        this.icoDetails = this.icoApiService.getIcoDetails()[0];

        if (this.icoDetails.IcoTotalExpected === null) {
          this.icoExpected = '';
        } else {
          this.icoExpected = this.icoDetails.IcoTotalExpected.trim();

          if (this.icoExpected !== '') {
            this.icoExpected = parseFloat(this.icoExpected);
          }
        }

        if (this.icoDetails.IcoTotalRaised === null) {
          this.icoRaised = '';
        } else {
          this.icoRaised = this.icoDetails.IcoTotalRaised.trim();

          if (this.icoRaised !== '') {
              this.icoRaised = parseFloat(this.icoRaised);
          }
        }

        if (this.icoDetails.IcoScale === null) {
          this.icoScale = '';
        } else {
          this.icoScale = this.icoDetails.IcoScale.trim();

          if (this.icoScale === '') {
              this.icoScale = '';
          } else {
              this.icoScale = parseFloat(this.icoScale);
          }
        }

        this.icoScaleCurrency = this.icoDetails.ScaleCurrency;

        if (this.icoScaleCurrency === null) {
          this.icoScaleCurrency = '';
        }

        this.icoExpectedCurrency = this.icoDetails.ExpectedCurrency;

        if (this.icoExpectedCurrency === null) {
          this.icoExpectedCurrency = '';
        }

        this.icoRaisedCurrency = this.icoDetails.RaisedCurrency;

        if (this.icoRaisedCurrency === null) {
          this.icoRaisedCurrency = '';
        } else if (this.icoRaisedCurrency === '$') {
          this.icoRaisedCurrency = 'USD';
        }

        this.icoStart = new Date(this.icoDetails.IcoStart);
        this.icoEnd = new Date(this.icoDetails.IcoEnd);

        if (this.icoStart > this.today) {
          this.icoPhase = 'Upcoming';
        }

        if (this.icoStart <= this.today && this.icoEnd >= this.today) {
          this.icoPhase = 'Ongoing';
        }

        if (this.icoEnd < this.today) {
          this.icoPhase = 'Past';
        }

        const lang = navigator.language;

        this.icoStart = this.icoStart.toLocaleDateString(lang);
        this.icoEnd = this.icoEnd.toLocaleDateString(lang);

        this.icoDetails.SocialArticles.forEach(article => {
          if (article.Type === 'article') {
              this.icoArticle = true;
          }
          if (article.Type === 'twitter') {
            this.icoTwitter = true;
          }
          if (article.Type === 'facebook') {
            this.icoFacebook = true;
          }
        });
        this.icoDetails.TeamMembers.forEach(member => {
          this.icoTeam = true;
        });
      }
    );
    window.scrollTo(0, 0);
  }

}
