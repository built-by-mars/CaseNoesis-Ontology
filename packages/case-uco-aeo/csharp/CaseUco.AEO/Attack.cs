// Adversary Engagement Ontology — attack module
namespace CaseUco.Ext.AEO.Attack
{
    public class AttackPattern
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/attack/AttackPattern";
        public List<Objective> HasObjective { get; set; } = new();
    }

    public class CyberKillChain
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/attack/CyberKillChain";
    }

    public class DefensePattern
    {
        public static readonly string ClassIri = "https://ontology.adversaryengagement.org/ae/attack/DefensePattern";
        public List<Objective> HasObjective { get; set; } = new();
    }

}