// Adversary Engagement Ontology — engagement module
namespace CaseUco.Ext.AEO.Engagement
{
    public class Access
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Access";
        public string? Name { get; set; }
    }

    public class Alert
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Alert";
        public string? Name { get; set; }
    }

    public class Beacon
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Beacon";
        public string? Name { get; set; }
    }

    public class Breadcrumb
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Breadcrumb";
        public List<UcoObject> BreadcrumbTargetObject { get; set; } = new();
        public List<UcoObject> HasCharacterization { get; set; } = new();
    }

    public class BreadcrumbTrail
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/BreadcrumbTrail";
        public List<UcoObject> BreadcrumbTargetObject { get; set; } = new();
        public List<Thread> HasBreadcrumb { get; set; } = new();
        public List<Objective> HasObjective { get; set; } = new();
    }

    public class DataSource
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/DataSource";
    }

    public class DataTarget
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/DataTarget";
    }

    public class DeceptionAction
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/DeceptionAction";
    }

    public class DeceptionObject
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/DeceptionObject";
        public List<UcoObject> HasAttackSurface { get; set; } = new();
        public List<UcoObject> HasCharacterization { get; set; } = new();
        public List<UcoObject> HasPerceptionCharacterization { get; set; } = new();
    }

    public class Decoy
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Decoy";
    }

    public class DenialAction
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/DenialAction";
    }

    public class Deploy
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Deploy";
        public string? Name { get; set; }
    }

    public class Event
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Event";
        public List<Dictionary> EventAttribute { get; set; } = new();
        public List<UcoObject> EventContext { get; set; } = new();
        public List<string> EventType { get; set; } = new();
        public List<string> EndTime { get; set; } = new();
        public List<string> StartTime { get; set; } = new();
    }

    public class HoneyObject
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/HoneyObject";
    }

    public class HoneyToken
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/HoneyToken";
    }

    public class Honeypot
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Honeypot";
        public List<object> HoneypotInteractionType { get; set; } = new();
    }

    public class Narrative
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Narrative";
        public List<UcoObject> HasObjective { get; set; } = new();
        public List<UcoObject> HasStoryline { get; set; } = new();
    }

    public class Obfuscate
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Obfuscate";
        public string? Name { get; set; }
    }

    public class PlannedEvent
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/PlannedEvent";
        public List<UcoObject> EventContext { get; set; } = new();
        public List<UcoObject> HasObjective { get; set; } = new();
    }

    public class PocketLitter
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/PocketLitter";
        public List<UcoObject> HasCharacterization { get; set; } = new();
    }

    public class Respond
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Respond";
        public string? Name { get; set; }
    }

    public class Storyline
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/engagement/Storyline";
        public List<Thread> HasEvent { get; set; } = new();
    }

}