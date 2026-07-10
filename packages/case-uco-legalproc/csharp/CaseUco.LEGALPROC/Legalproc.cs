// Legal Process and Procedure Extension — legalproc module
namespace CaseUco.Ext.LEGALPROC.Legalproc
{
    public class ChargingInstrument
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/ChargingInstrument";
        public string? InstrumentType { get; set; }
    }

    public class CriminalCharge
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/CriminalCharge";
        public List<ChargingInstrument> AssertedIn { get; set; } = new();
        public string? ChargeClassification { get; set; }
        public List<string> ChargeDisposition { get; set; } = new();
        public string? CountLabel { get; set; }
        public List<ulong> CountNumber { get; set; } = new();
        public List<CriminalCharge> ObjectOffense { get; set; } = new();
        public string? OffenseForm { get; set; }
        public List<string> StatuteCitation { get; set; } = new();
    }

    public class CriminalProceeding
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/CriminalProceeding";
        public string? ProceedingType { get; set; }
    }

    public class ForfeitureOrder
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/ForfeitureOrder";
        public string? CurrencyCode { get; set; }
        public decimal? MonetaryAmount { get; set; }
    }

    public class Plea
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/Plea";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? PleaType { get; set; }
    }

    public class RestitutionOrder
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/RestitutionOrder";
        public string? CurrencyCode { get; set; }
        public decimal? MonetaryAmount { get; set; }
    }

    public class Sentence
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/Sentence";
        public string? SentenceStatus { get; set; }
        public string? SentenceTerm { get; set; }
    }

    public class Verdict
    {
        public static readonly string ClassIri = "http://example.org/ontology/legalproc/Verdict";
        public List<CriminalCharge> ConcernsCharge { get; set; } = new();
        public string? VerdictType { get; set; }
    }

}