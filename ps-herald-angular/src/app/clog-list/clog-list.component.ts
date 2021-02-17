import { Component, OnInit } from '@angular/core';
import { SlogDataService } from '../slog-data.service'
import { MessageService } from '../message.service';
import { Log } from '../log';


@Component({
  selector: 'app-clog-list',
  templateUrl: './clog-list.component.html',
  styleUrls: ['./clog-list.component.css']
})
export class ClogListComponent implements OnInit {
  logs: Log[];
  constructor(private slogdataService: SlogDataService,
                       private messageService: MessageService ) { }

  ngOnInit(): void {
    this.slogdataService.refreshNeeded$
      .subscribe(() => {
        this.getLog();
      });
    this.getLog()
  }

  getLog(): void {
    this.slogdataService.getData().subscribe({
      next: data => {
        this.logs = data;
      },
      error: error => {
        this.messageService.add("Option get ERR Handler called with " + error)
        console.error('There was an error!', error);
      }
  });
  }

  
}
