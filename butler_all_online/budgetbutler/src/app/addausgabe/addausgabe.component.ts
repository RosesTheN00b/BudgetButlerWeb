import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { EinzelbuchungserviceService } from '../einzelbuchungservice.service';
import { KategorieService } from '../kategorie.service';
import { MyErrorStateMatcher } from '../matcher';
import { EinzelbuchungAnlegen } from '../model';


@Component({
  selector: 'app-addausgabe',
  templateUrl: './addausgabe.component.html',
  styleUrls: ['./addausgabe.component.css']
})
export class AddausgabeComponent implements OnInit {

  datum = new FormControl(new Date(), Validators.required);
  name = new FormControl('', Validators.required);
  kategorie = new FormControl('', Validators.required);
  wert = new FormControl('', Validators.required);


  kategorien: Observable<string[]>;
  einzelbuchungMatcher = new MyErrorStateMatcher();

  constructor(
    private einzelbuchungsService: EinzelbuchungserviceService,
    private kategorieService: KategorieService) { }

  ngOnInit() {
    this.kategorien = this.kategorieService.getAll();
  }

  private isEinzelbuchungFormOk(): boolean {
    return this.datum.valid &&
      this.name.valid &&
      this.kategorie.valid &&
      this.wert.valid
  }

  hinzufuegen() {
    if (!this.isEinzelbuchungFormOk()) {
      return;
    }

    const neueBuchung: EinzelbuchungAnlegen = {
      name: this.name.value,
      datum: this.datum.value,
      kategorie: this.kategorie.value,
      wert: this.wert.value * -1
    };
    this.datum.reset(new Date());
    this.name.reset();
    this.kategorie.reset(this.kategorien[0]);
    this.wert.reset();
    this.einzelbuchungsService.save(neueBuchung);
  }
}
