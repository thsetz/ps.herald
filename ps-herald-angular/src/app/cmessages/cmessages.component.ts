import { Component, OnInit } from '@angular/core';
import { MessageService } from '../message.service';

@Component({
  selector: 'app-cmessages',
  templateUrl: './cmessages.component.html',
  styleUrls: ['./cmessages.component.css']
})
export class CmessagesComponent implements OnInit {

  constructor(public messageService: MessageService) { }

  ngOnInit(): void {
  }

}
