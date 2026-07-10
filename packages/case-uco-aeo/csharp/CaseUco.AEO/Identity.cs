// Adversary Engagement Ontology — identity module
namespace CaseUco.Ext.AEO.Identity
{
    public class Persona
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/identity/Persona";
    }

    public class Team
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/identity/Team";
        public List<Objective> HasObjective { get; set; } = new();
    }

}