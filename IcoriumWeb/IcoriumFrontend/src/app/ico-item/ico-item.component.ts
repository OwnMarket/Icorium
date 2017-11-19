import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-ico-item',
  templateUrl: './ico-item.component.html',
  styleUrls: ['./ico-item.component.css']
})
export class IcoItemComponent implements OnInit {
  @Input() icos;
  @Input() type;

  constructor() { }

  ngOnInit() {
    window.scrollTo(0, 0);
  }

  onIcoClick(event) {
    const scrol = event.pageY;
    localStorage.setItem('scrol', scrol);
  }

}
