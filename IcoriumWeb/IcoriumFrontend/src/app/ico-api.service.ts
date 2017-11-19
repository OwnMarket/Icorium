import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/map';
import { environment } from '../environments/environment';

@Injectable()
export class IcoApiService {
  private currentIcos = [];
  private upcomingIcos = [];
  private pastIcos = [];
  private companies = [];
  private currentIcosPage = 1;
  private upcomingIcosPage = 1;
  private pastIcosPage = 1;
  private icoLimit = environment.icoLimit;
  private companyName = '';
  private currentIcosCount = 0;
  private upcomingIcosCount = 0;
  private pastIcosCount = 0;
  private icoDetails = [];
  private icoId = 0;
  private emailSendResponse;
  viewCurrentIcos = new Subject<void>();
  viewUpcomingIcos = new Subject<void>();
  viewPastIcos = new Subject<void>();
  viewCurrentIcosCount = new Subject<void>();
  viewUpcomingIcosCount = new Subject<void>();
  viewPastIcosCount = new Subject<void>();
  viewIcoDetails = new Subject<void>();
  viewCompanies = new Subject<void>();
  viewSendEmail = new Subject<void>();
  http: Http;

  constructor(http: Http) {
    this.http = http;
  }

  fetchCurrentIcos() {
    this.http.get('http://api.icorium.io/current-icos/?page=' + this.currentIcosPage + '&limit=' + this.icoLimit +
                  '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewCurrentIcos = data.map((ico) => {
        return ico;
      });
      return viewCurrentIcos;
    })
    .subscribe(
      (data) => {
        this.currentIcos = this.currentIcos.concat(data);
        this.currentIcosPage ++;
        this.viewCurrentIcos.next();
      }
    );
  }

  fetchUpcomingIcos() {
    this.http.get('http://api.icorium.io/upcoming-icos/?page=' + this.upcomingIcosPage + '&limit=' +
                  this.icoLimit + '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewUpcomingIcos = data.map((ico) => {
        return ico;
      });
      return viewUpcomingIcos;
    })
    .subscribe(
      (data) => {
        this.upcomingIcos = this.upcomingIcos.concat(data);
        this.upcomingIcosPage ++;
        this.viewUpcomingIcos.next();
      }
    );
  }

  fetchCurrentIcosCount() {
    this.http.get('http://api.icorium.io/icos-count/?type=current' + '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewCurrentIcosCount = data.TotalIcos;
      return viewCurrentIcosCount;
    })
    .subscribe(
      (data) => {
        this.currentIcosCount = data;
        this.viewCurrentIcosCount.next();
      }
    );
  }

  fetchUpcomingIcosCount() {
    this.http.get('http://api.icorium.io/icos-count/?type=upcoming' + '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewUpcomingIcosCount = data.TotalIcos;
      return viewUpcomingIcosCount;
    })
    .subscribe(
      (data) => {
        this.upcomingIcosCount = data;
        this.viewUpcomingIcosCount.next();
      }
    );
  }

  fetchPastIcosCount() {
    this.http.get('http://api.icorium.io/icos-count/?type=past' + '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewPastIcosCount = data.TotalIcos;
      return viewPastIcosCount;
    })
    .subscribe(
      (data) => {
        this.pastIcosCount = data;
        this.viewPastIcosCount.next();
      }
    );
  }

  fetchPastIcos() {
    this.http.get('http://api.icorium.io/past-icos/?page=' + this.pastIcosPage + '&limit=' +
                  this.icoLimit + '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewPastIcos = data.map((ico) => {
        return ico;
      });
      return viewPastIcos;
    })
    .subscribe(
      (data) => {
        this.pastIcos = this.pastIcos.concat(data);
        this.pastIcosPage ++;
        this.viewPastIcos.next();
      }
    );
  }

  fetchIcoDetails() {
    this.http.get('http://api.icorium.io/ico/?id=' + this.icoId)
    .map((response: Response) => {
      const data = response.json();
      const viewIcoDetails = data.map((ico) => {
        return ico;
      });
      return viewIcoDetails;
    })
    .subscribe(
      (data) => {
        this.icoDetails = data;
        this.viewIcoDetails.next();
      }
    );
  }

  fetchIcos() {
    this.http.get('http://api.icorium.io/current-icos/?page=' + this.currentIcosPage + '&limit=' + this.icoLimit +
                  '&company=' + this.companyName)
    .map((response: Response) => {
      const data = response.json();
      const viewCurrentIcos = data.map((ico) => {
        return ico;
      });
      return viewCurrentIcos;
    })
    .subscribe(
      (data) => {
        this.currentIcos = this.currentIcos.concat(data);
        this.currentIcosPage ++;
        this.viewCurrentIcos.next();
      }
    );
  }

  fetchCompanies() {
    this.http.get('http://api.icorium.io/company/')
    .map((response: Response) => {
      const data = response.json();
      const viewCompanies = data.map((company) => {
        return company;
      });
      return viewCompanies;
    })
    .subscribe(
      (data) => {
        this.companies = data;
        this.viewCompanies.next();
      }
    );
  }

  sendEmail(name, email, content) {
    const getData = 'name=' + name + '&email=' + email + '&content=' + content;

    this.http.get('http://api.icorium.io/contact-email/?' + getData)
    .map((response: Response) => {
      const data = response.json();
      const viewSendEmail = data.Success;
      return viewSendEmail;
    })
    .subscribe(
      (data) => {
        this.emailSendResponse = data;
        this.viewSendEmail.next();
      }
    );
  }

  loadMoreIcos(icoType) {
    if (icoType === 'current') {
       this.fetchCurrentIcos();
    } else if (icoType === 'upcoming') {
      this.fetchUpcomingIcos();
    } else if (icoType === 'past') {
      this.fetchPastIcos();
    }
  }

  getIcoDetails() {
    return this.icoDetails.slice();
  }

  getCurrentIcos() {
    return this.currentIcos.slice();
  }

  getUpcomingIcos() {
    return this.upcomingIcos.slice();
  }

  getPastIcos() {
    return this.pastIcos.slice();
  }

  getCurrentIcosCount() {
    return this.currentIcosCount;
  }

  getUpcomingIcosCount() {
    return this.upcomingIcosCount;
  }

  getPastIcosCount() {
    return this.pastIcosCount;
  }

  getCompanies() {
    return this.companies.slice();
  }

  getSendEmailResponse() {
    return this.emailSendResponse;
  }

  setCompanyName(company) {
    this.companyName = company;
  }

  setIcoId(icoId) {
    this.icoId = icoId;
  }

  resetIcos() {
    this.currentIcos = [];
    this.upcomingIcos = [];
    this.pastIcos = [];
    this.currentIcosPage = 1;
    this.upcomingIcosPage = 1;
    this.pastIcosPage = 1;
  }
}
