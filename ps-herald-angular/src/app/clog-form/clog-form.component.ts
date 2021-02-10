import { Component, OnInit } from '@angular/core';
import { Searchvalues } from './search-values'

@Component({
  selector: 'app-clog-form',
  templateUrl: './clog-form.component.html',
  styleUrls: ['./clog-form.component.css']
})
export class ClogFormComponent implements OnInit {

  model = new Searchvalues();

  submitted = false;
  onSubmit() {this.submitted = true}
  // TODO: Remove this when we're done
  get diagnostic() { return JSON.stringify(this.model); }

  constructor() { }
  ngOnInit(): void {
  }

}
