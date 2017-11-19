import { Component, OnInit, OnDestroy, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgModule } from '@angular/core';
import {PageScrollConfig} from 'ng2-page-scroll';
import { IcoApiService } from '../ico-api.service';

@Component({
  selector: 'app-ico-list',
  templateUrl: './ico-list.component.html',
  styleUrls: ['./ico-list.component.css']
})
export class IcoListComponent implements OnInit, OnDestroy, AfterViewInit {
  currentIcos = [];
  upcomingIcos = [];
  pastIcos = [];
  currentIcosCounter;
  upcomingIcosCounter;
  pastIcosCounter;
  activatedRoute: ActivatedRoute;
  icoApiService: IcoApiService;
  currentSubscription;
  upcomingSubscription;
  pastSubscription;
  currentCountSubscription;
  upcomingCountSubscription;
  pastCountSubscription;

  constructor(activatedRoute: ActivatedRoute, icoApiService: IcoApiService) {
    this.activatedRoute = activatedRoute;
    this.icoApiService = icoApiService;

    PageScrollConfig.defaultScrollOffset = 50;
  }

  ngOnInit() {
    this.activatedRoute.params.subscribe(
      (params) => {
        this.currentIcos = this.icoApiService.getCurrentIcos();
        this.upcomingIcos = this.icoApiService.getUpcomingIcos();
        this.pastIcos = this.icoApiService.getPastIcos();

        this.currentIcosCounter = this.icoApiService.getCurrentIcosCount();
        this.upcomingIcosCounter = this.icoApiService.getUpcomingIcosCount();
        this.pastIcosCounter = this.icoApiService.getPastIcosCount();
      }
    );
    this.currentSubscription = this.icoApiService.viewCurrentIcos.subscribe(
      () => {
        this.currentIcos = this.icoApiService.getCurrentIcos();
      }
    );
    this.upcomingSubscription = this.icoApiService.viewUpcomingIcos.subscribe(
      () => {
        this.upcomingIcos = this.icoApiService.getUpcomingIcos();
      }
    );
    this.pastSubscription = this.icoApiService.viewPastIcos.subscribe(
      () => {
        this.pastIcos = this.icoApiService.getPastIcos();
      }
    );
    this.upcomingCountSubscription = this.icoApiService.viewUpcomingIcosCount.subscribe(
      () => {
        this.upcomingIcosCounter = this.icoApiService.getUpcomingIcosCount();
      }
    );
    this.currentCountSubscription = this.icoApiService.viewCurrentIcosCount.subscribe(
      () => {
        this.currentIcosCounter = this.icoApiService.getCurrentIcosCount();
      }
    );
    this.pastCountSubscription = this.icoApiService.viewPastIcosCount.subscribe(
      () => {
        this.pastIcosCounter = this.icoApiService.getPastIcosCount();
      }
    );
  }

  onCurrentIcoClick() {
    this.icoApiService.loadMoreIcos('current');
    this.currentIcos = this.icoApiService.getCurrentIcos();
  }

  onUpcomingIcoClick() {
    this.icoApiService.loadMoreIcos('upcoming');
    this.upcomingIcos = this.icoApiService.getUpcomingIcos();
  }

  onPastIcoClick() {
    this.icoApiService.loadMoreIcos('past');
    this.pastIcos = this.icoApiService.getPastIcos();
  }

  ngAfterViewInit()  {
    const scrollPosition = parseInt(localStorage.getItem('scrol'), 10) - 80;
    window.scrollTo(0, scrollPosition);
  }

  ngOnDestroy() {
    this.currentSubscription.unsubscribe();
  }
}
