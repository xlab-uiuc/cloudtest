using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System.Reflection; 

public class FunctionCallExtractor
{
    public static void ExtractFunctionCalls(string filePath)
    {
        Console.WriteLine(); 
        
        // Create syntax tree
        var code = File.ReadAllText(filePath);
        var tree = CSharpSyntaxTree.ParseText(code);
        var root = tree.GetRoot();

        // Load methods for Azure assemblies
        string[] namespaces = {"Azure.Storage.Blobs", "Azure.Storage.Queues", "Azure.Data.Tables"}; 
        List<string> method_names = new List<string>(); 

        foreach(var ns in namespaces){
            try{
                var assembly = Assembly.Load(ns); 
                Type[] types = assembly.GetTypes(); 
                foreach(var type in types){
                    if(type.IsClass){    
                        var methods = type.GetMethods(); 
                        foreach(var method in methods){
                            method_names.Add(method.Name);  
                        }
                    }
                }
            } catch {
                Console.WriteLine($"Could not load assembly for {ns}"); 
            }
        }

        // Get namespaces used in file
        var usingDirectives = root.DescendantNodes().OfType<UsingDirectiveSyntax>().ToList();
        var importedNamespaces = usingDirectives
            .Select(u => u.Name.ToString())
            .Distinct()
            .ToList();

        Console.WriteLine($"Azure namspaces used:"); 
        foreach(var ns in importedNamespaces){
            if (namespaces.Contains(ns)){
                Console.WriteLine(ns); 
            }
        }
        Console.WriteLine(); 

        // Get function calls
        var functionCalls = root.DescendantNodes().OfType<InvocationExpressionSyntax>()
            .Select(invocation => invocation.Expression)
            .Distinct()
            .ToList();

        string[] azure_functions = Array.Empty<string>(); 
        Console.WriteLine("List of function calls:");
        foreach (var functionCall in functionCalls)
        {   
            var function_name_list = functionCall.ToString().Split("."); 
            var function_name = function_name_list[function_name_list.Length - 1]; 
            if(method_names.Contains(function_name)){
                Console.WriteLine($"Function: {function_name}");
            }
        }
    }
}

public class Program
{
    public static void Main()
    {
        string[] filePaths = Directory.GetFiles("../alpakka"); 
        foreach(var path in filePaths){
            Console.WriteLine(path); 
            FunctionCallExtractor.ExtractFunctionCalls(path);
            Console.WriteLine(); 
        }
    }
}








  


