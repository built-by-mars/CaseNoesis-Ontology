//! Legal Process and Procedure Extension — legalproc module

use serde::Serialize;

/// A charging instrument is a formal document that initiates or amends criminal charges against one or more defendants, suc
#[derive(Debug, Clone, Serialize, Default)]
pub struct ChargingInstrument {
    pub instrument_type: Option<String>,
}

impl ChargingInstrument {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/ChargingInstrument" }
}

/// A criminal charge is a formal accusation, stated as one or more counts within a charging instrument, that a person commi
#[derive(Debug, Clone, Serialize, Default)]
pub struct CriminalCharge {
    pub asserted_in: Vec<ChargingInstrument>,
    pub charge_classification: Option<String>,
    pub charge_disposition: Vec<String>,
    pub count_label: Option<String>,
    pub count_number: Vec<u64>,
    pub object_offense: Vec<CriminalCharge>,
    pub offense_form: Option<String>,
    pub statute_citation: Vec<String>,
}

impl CriminalCharge {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/CriminalCharge" }
}

/// A criminal proceeding is a formal event in a criminal case conducted before a tribunal, such as an arraignment, detentio
#[derive(Debug, Clone, Serialize, Default)]
pub struct CriminalProceeding {
    pub proceeding_type: Option<String>,
}

impl CriminalProceeding {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/CriminalProceeding" }
}

/// A forfeiture order is an order, or pre-conviction allegation, requiring surrender to the state of property involved in o
#[derive(Debug, Clone, Serialize, Default)]
pub struct ForfeitureOrder {
    pub currency_code: Option<String>,
    pub monetary_amount: Option<f64>,
}

impl ForfeitureOrder {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/ForfeitureOrder" }
}

/// A plea is a defendant's formal answer to a criminal charge. See Federal Rule of Criminal Procedure 11 (https://www.law.c
#[derive(Debug, Clone, Serialize, Default)]
pub struct Plea {
    pub concerns_charge: Vec<CriminalCharge>,
    pub plea_type: Option<String>,
}

impl Plea {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/Plea" }
}

/// A restitution order is an order or request that an offender compensate victims for losses caused by the offense, monetar
#[derive(Debug, Clone, Serialize, Default)]
pub struct RestitutionOrder {
    pub currency_code: Option<String>,
    pub monetary_amount: Option<f64>,
}

impl RestitutionOrder {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/RestitutionOrder" }
}

/// A sentence is a penalty recommended by a party or imposed by a tribunal upon conviction of a criminal charge, including 
#[derive(Debug, Clone, Serialize, Default)]
pub struct Sentence {
    pub sentence_status: Option<String>,
    pub sentence_term: Option<String>,
}

impl Sentence {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/Sentence" }
}

/// A verdict is a finder of fact's formal determination on a criminal charge, such as a jury's finding of guilty or not gui
#[derive(Debug, Clone, Serialize, Default)]
pub struct Verdict {
    pub concerns_charge: Vec<CriminalCharge>,
    pub verdict_type: Option<String>,
}

impl Verdict {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/legalproc/Verdict" }
}
