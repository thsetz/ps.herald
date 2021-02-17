import { Component, OnInit } from '@angular/core';
//import { Searchvalues } from '../search-values'
//import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { MessageService } from '../message.service';
import { SlogDataService } from '../slog-data.service';

@Component({
  selector: 'app-clog-form',
  templateUrl: './clog-form.component.html',
  styleUrls: ['./clog-form.component.css']
})
export class ClogFormComponent implements OnInit {

  onSubmit() {
    this.slogdataService.refresh();
  }
  // TODO: Remove this when we're done
  get diagnostic() { return JSON.stringify(this.slogdataService.search_tuple); }

  constructor(public slogdataService: SlogDataService,
              private messageService: MessageService) { 
  }
  ngOnInit(): void { }

}
