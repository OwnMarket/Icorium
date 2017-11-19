import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';

import { IcoApiService } from './ico-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  router: Router;
  activatedRoute: ActivatedRoute;
  icoApiService: IcoApiService;
  page;

  constructor(router: Router, activatedRoute: ActivatedRoute, icoApiService: IcoApiService) {
    this.router = router;
    this.activatedRoute = activatedRoute;
    this.icoApiService = icoApiService;
  }

  ngOnInit() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
         this.page = event.url.substring(1);
      }
    });

    this.icoApiService.fetchCurrentIcos();
    this.icoApiService.fetchUpcomingIcos();
    this.icoApiService.fetchPastIcos();
    this.icoApiService.fetchCurrentIcosCount();
    this.icoApiService.fetchUpcomingIcosCount();
    this.icoApiService.fetchPastIcosCount();
    this.icoApiService.fetchCompanies();
  }
}
