import { Component, OnInit } from '@angular/core';

import { IcoApiService } from '../ico-api.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {
  icoApiService: IcoApiService;
  requestSent = '';
  firstName = '';
  lastName = '';
  email = '';
  request = '';
  sendEmailResponse;
  sentEmailSubscription;

  constructor(icoApiService: IcoApiService) {
    this.icoApiService = icoApiService;
  }

  ngOnInit() {
    this.sentEmailSubscription = this.icoApiService.viewSendEmail.subscribe(
      () => {
        this.sendEmailResponse = this.icoApiService.getSendEmailResponse();
        if (this.sendEmailResponse) {
          this.requestSent = 'Thank you for contacting us! We will get back to you shortly.';
        } else {
          this.requestSent = 'Ups! Something went wrong. Please try again later.';
        }
      }
    );
    window.scrollTo(0, 0);
  }

  onSubmit(submittedForm) {
    this.requestSent = '';

    if (submittedForm.invalid) {
      return;
    }
    this.requestSent = 'Sending email..';
    const name = submittedForm.value.first_name + ' ' + submittedForm.value.last_name;
    this.icoApiService.sendEmail(name, submittedForm.value.email, submittedForm.value.request);
  }
}
