import { Component, OnInit } from '@angular/core';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Ng2PageScrollModule } from 'ng2-page-scroll';

import { IcoApiService } from '../ico-api.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  icoApiService: IcoApiService;
  company = '';
  companies = [];
  companyList = [];
  mycompanies = ['test', 'this'];
  companySubscription;

  constructor(icoApiService: IcoApiService) {
    this.icoApiService = icoApiService;
  }

  ngOnInit() {
    this.companySubscription = this.icoApiService.viewCompanies.subscribe(
      () => {
          this.companies = this.icoApiService.getCompanies();
          for (let i = 0; i < this.companies.length; i++) {
            this.companyList = this.companies[i];
          }
        }
    );
  }

  onCompanySelected(value) {
    this.company = value;
    this.searchIcos(this.company);
  }

  onClearClicked() {
    this.company = '';
    this.searchIcos(this.company);
  }

  searchIcos(companyName) {
    this.icoApiService.setCompanyName(companyName);
    this.icoApiService.resetIcos();
    this.icoApiService.fetchCurrentIcos();
    this.icoApiService.fetchUpcomingIcos();
    this.icoApiService.fetchPastIcos();
    this.icoApiService.fetchCurrentIcosCount();
    this.icoApiService.fetchUpcomingIcosCount();
    this.icoApiService.fetchPastIcosCount();
  }

  onSubmit(submittedForm) {
    if (submittedForm.invalid) {
      return;
    }
    this.searchIcos(submittedForm.value.company);
  }
}
