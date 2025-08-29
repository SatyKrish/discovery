# How To Build a Durable AI Agent with Temporal and Python

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 TutorialsAI tutorialsHow To Build a Durable AI Agent with Temporal and PythonHow To Build a Durable AI Agentwith Temporal and PythonLast updated on Jul 24, 2025 byMason EggerTags:AISeriesIntroductionAn AI agent uses large language models (LLMs) to plan andexecute steps towards a goal. While attempting to reach its goal,the agent can perform actions such as searching for information,interacting with external services, and even calling other agents.However, building reliable AI agents presents various challenges.Network failures, long-running workflows, observability challenges,and more make building AI agents a textbook distributed systemsproblem.Temporal orchestrates long-running workflows, automaticallyhandles failure cases from network outages to server crashes,provides insights into your running applications, and more. Thesefeatures provide the resiliency and durability necessary to buildreliable agents that users can rely on.In this tutorial you'll build an AI agent using Temporal that searchesfor events in a given city, helps you book a plane ticket, andcreates an invoice for the trip. The user will interact with thisapplication through a chatbot interface, communicating with theagent using natural language. Throughout this tutorial you willimplement the following components:
Ask AI

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 tools the agent will use to search for events, findflights, and generate invoices.An agent goal that will specify what overall task the agent istrying to achieve and what tools it is allowed to use.Temporal Workflows that will orchestrate multi-turnconversations and ensure durability across failuresTemporal Activities that execute tools and language modelcalls with automatic retry logicA FastAPI backend that connects the web interface to yourTemporal WorkflowsA web-based chat interface that allows users to interact withthe agentBy the end of this tutorial, you will have a modular, durable AI agentthat you can extend to run any goal using any set of tools. Youragent will be able to recover from failure, whether it's a hardwarefailure, a tool failure, or an LLM failure. And you'll be able to useTemporal to build reliable AI applications that maintain state andprovide consistent user experiences.You can find the code for this tutorial on GitHub in the tutorial-temporal-ai-agent repository.PrerequisitesBefore starting this tutorial, ensure that you have the following onyour local machine:RequiredThe Temporal CLI development service installed and verified.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Python 3.9 or higher installed. Verify your installation byrunning python3 --version in your terminal.The uv package and project manager installed. uv is amodern, fast Python package manager that will handle virtualenvironments and dependencies.The command line tool curl installed for downloading certainfiles.Node.js 18 or higher installed. You can verify your installationwith node --version and npm --version.An OpenAI API key saved securely where you can access it.You may need to create an OpenAI account first. You will usethis key to configure the LLM integration.NOTEOpenAI API Keys require purchasing credits to use. You cansucceed with this tutorial with minimal credits; in ourexperience, less than $1 will suffice.OptionalYou can opt to use real API services for your tools, or use providedmock functions.A free RapidAPI Sky Scrapper API Key saved securely whereyou can access it. You will use this to search for flights.A free Stripe Account with a configured sandbox. You will usethis to generate fake invoices for the flights that are beingbooked.Concepts

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Additionally, this tutorial assumes you have basic familiarity with:Programming ConceptsTemporal fundamentals such as Workflows, Activities,Workers, Signals, and QueriesPython fundamentals such as functions, classes, async/awaitsyntax, and virtual environmentsCommand line interface and running commands in a terminalor command promptREST API concepts including HTTP requests and JSONresponsesHow to set and use environment variables in your operatingsystemAI ConceptsA Mental Model for Agentic AI ApplicationsBuilding an agentic system that's actually production readyWhy Agentic Flows Need Distributed SystemsSetting up your developmentenvironmentBefore you start coding, you need to set up your Python developerenvironment. In this step, you will set up your project structure,install the necessary Python packages, and configure the Pythonenvironment needed to build your AI agent.First, create your project using uv:$ uv init temporal-ai-agent --python ">=3.9"

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

uv is a modern Python project and packaging tool that sets up aproject structure for you. Running this command creates thefollowing default Python package structure for you:
It automatically runs a git init command for you, provides youwith the default .gitignore for Python, creates a 
.python-
version file that has the project's default Python version, aREADME.md, a Hello World main.py program, and apyproject.toml file for managing the projects packages andenvironment.Next, change directories into your newly created project:You won't need the main.py file, so delete it:Next, create your virtual environment by running the followingcommand:$ uv init temporal-ai-agent --python ">=3.9"
temporal-ai-agent/├── .gitignore├── .python-version├── main.py├── README.md├── pyproject.toml└── uv.lock
```
$ cd temporal-ai-agent$ rm main.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This creates a virtual environment named .venv in the currentworking directory.Now that you have a virtual environment created, add thedependencies needed to build your AI agent system:This installs all the necessary packages:python-dotenv - For loading environment variables from a.env filefastapi and uvicorn - Web framework and server for theAPI backendjinja2 - Template enginelitellm - Unified interface for different language modelprovidersstripe - Payment processing library for the invoicegeneration demotemporalio - The Temporal Python SDKrequests - HTTP library for API callsFinally, add the following lines to the end of yourpyproject.toml file:uv venv
```
$ uv add python-dotenv fastapi jinja2 litellm stripe temporalio uvicorn requests
[build-system]requires = ["hatchling"]build-backend = "hatchling.build"

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This configures uv as to which packages to include and enable forexecution. You will create these packages later in the tutorial.
Next, create a .env file to store your configuration:Next, copy the following configuration to your .env file.# Tell hatchling what to include[tool.hatch.build.targets.wheel]packages = ["activities", "api", "models", "prompts", "shared", "tools", "workflows"]The pyproject.toml is complete and will need no morerevisions. You can review the complete file and copy thecode here$ touch .env# LLM ConfigurationLLM_MODEL=openai/gpt-4oLLM_KEY=YOUR_OPEN_AI_KEY# Set if the user should click a Confirm button in the UI to allow the tool# to executeSHOW_CONFIRM=True# Temporal ConfigurationTEMPORAL_ADDRESS=localhost:7233TEMPORAL_NAMESPACE=defaultTEMPORAL_TASK_QUEUE=agent-task-queue

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Once copied, replace YOUR_OPEN_API_KEY with your OpenAI APIkey. Setting SHOW_CONFIRM=True requires the user to confirmeach tool prior to it being executed. This will allow you to see whatthe agent is doing step by step. These are the only two mandatoryvariables to set. This tutorial provides both an ability to createpseudo tools that perform simulations, or tools that use externalAPIs to achieve their goals. If you plan on using the RapidAPISkyScraper API to look up flight data or the Stripe API to generatean invoice, you can uncomment these lines and provide the APIkeys here.Additionally, if you plan on connecting to Temporal Cloud, you willneed to update the TEMPORAL_ADDRESS andTEMPORAL_NAMESPACE parameters to connect to your Temporal# (Optional) - Uncomment both lines and set RAPIDAPI_KEY if you plan on # using the real flights API# RAPIDAPI_KEY=YOUR_RAPID_API_KEY# RAPIDAPI_HOST_FLIGHTS=sky-scrapper.p.rapidapi.com# (Optional) - Uncomment and set STRIPE_API_KEY if you plan on using the Stripe# API to generate a fake invoice# STRIPE_API_KEY=YOUR_STRIPE_API_KEY# Uncomment if connecting to Temporal Cloud using mTLS (not needed for local dev server)# TEMPORAL_TLS_CERT='path/to/cert.pem'# TEMPORAL_TLS_KEY='path/to/key.pem'# Uncomment if connecting to Temporal Cloud using API key (not needed for local dev server)# TEMPORAL_API_KEY=abcdef1234567890

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Cloud instance. You will also need to uncomment and set theTEMPORAL_TLS or TEMPORAL_API_KEY variables, depending onwhich authentication method you are using.NOTEAs this project is using LiteLLM, it supports various differentLLM providers. This tutorial will use OpenAI's gpt-4o, but youare welcome to use whichever LLM you wish, so long as it issupported by LiteLLM.At this point, you have configured your developer environment toinclude a Python project managed by uv with all requireddependencies to build a Temporal powered agentic AI, and allnecessary environment variables.Now that you have set up your developer environment, you willbuild the tools that your agent will use to perform the various tasksit needs to accomplish its goal.Constructing the agenttoolkitIn this step, you will acquire the tools that will be available to youragent. Agents are aware of the tools they have available to themwhile attempting to achieve their goal. The agent will evaluatewhich tools are available and execute a tool if the agent believes itwill provide the result the agent needs to progress in its task.These tools can take various forms, but in this tutorial they'reimplemented as a series of independent Python scripts thatprovide data in a specific format that the agent can process. There

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

are three tools: a find_events tool, a search_flights tool,and a create_invoice tool. The LLM will decide when to useeach tool as it interacts with the user who is trying to find an eventand book a flight to attend it. You could implement these toolsyourself, or you could download a tool and provide it to an agent.For this tutorial, you will download the tools directly from thecompanion GitHub repository.Setting up the tools packageTo get started, first create the directory for your tools modules:Then change directories into it:However, for this to be an importable tools package, you will needto add a __init__.py file. It can be blank for now, so create itwith the following command:Now that you have set up the structure for your tools package,you'll acquire and test the tools needed to have the agent succeedwith its goal.Acquiring the find_events tool$ mkdir tools$ cd tools
```
$ touch __init__.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The find_events tool searches for events within a given cityduring a certain time of year. The tool takes a month and city asinputs and provides events for not only the month that wasprovided, but the months before and after the given month as well.The LLM will use this tool to search for events when helping theuser plan their trip. This tool doesn't use an API, but rathersimulates looking events up in a data store using mock data.First, create a data directory within the tools directory to storethe sample event data and change directories into it:Next, run the following command to download the sample datafrom the companion GitHub repository:
You can confirm you have the correct data by running the followingcommand to sample the file and comparing it to the output:$ mkdir datacd data
```
$ curl -o find_events_data.json https://raw.githubusercontent.com/temporal-community/tutorial-temporal-ai-agent/main/tools/data/find_events_data.json
```
$ head -8 find_events_data.json```
{  "New York": [    {      "eventName": "Winter Jazzfest",      "dateFrom": "2025-01-10",

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

NOTEIf the dates appear to be far in the past, don't worry. There islogic within the find_events tool that automatically adjuststhe date to ensure that no dates can be presented that are inthe past.Next, change directories back up one directory to the toolsdirectory:Now that you have the data, download the find_events toolusing the command:
Open the file and explore the logic; you should never download afile from the internet and just trust it.Try to answer the following questions about the codebase:Where in the code does it determine the adjacent months?      "dateTo": "2025-01-19",      "description": "A multi-venue jazz festival featuring emerging and established artists performing across Greenwich Village venues."    }
```,
```
$ cd ..
```
$ curl -o find_events.py https://raw.githubusercontent.com/temporal-community/tutorial-temporal-ai-agent/main/tools/find_events.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

How does the tool prevent the data fromfind_events_data.json being presented with a date thathas already passed?What is the schema for the data that will be returned?Once you have finished reviewing the code, navigate to the rootdirectory of your project and create a scripts directory for testingthis tool. The root of your project should be one level higher yourcurrent directory, so you can get there by running the followingcommand:Create the scripts directory:Now create a test script named find_events_test.py in thescripts directory and add the following to test your script:
This script will check for events in Austin, TX in the month ofDecember.$ cd ..$ mkdir scripts
import jsonfrom tools.find_events import find_eventsif __name__ == "__main__":    search_args = ```
{"city": "Austin", "month": "December"}
```    results = find_events(search_args)    print(json.dumps(results, indent=2))

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

From the root of your project, run the script using the followingcommand to verify it's configured correctly:You should see the following output:$ uv run scripts/find_events_test.py```
{  "note": "Returning events from December plus one month either side (i.e., November, December, January).",  "events": [    {      "city": "Austin",      "eventName": "Austin Celtic Festival",      "dateFrom": "2025-11-08",      "dateTo": "2025-11-09",      "description": "Celebration of Celtic culture featuring traditional music, dance, crafts, and Irish food.",      "month": "previous month"    }
```,    ```
{      "city": "Austin",      "eventName": "Trail of Lights",      "dateFrom": "2025-12-05",      "dateTo": "2025-12-23",      "description": "Holiday light display in Zilker Park featuring festive decorations, food vendors, and family activities.",      "month": "requested month"    }
```  ]}

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Now that you have the find_events tool functioning, it's time todo the same for the search_flights tool.Acquiring the search_flights toolThe search_flights tool searches roundtrip flights to adestination. The tool takes the origin, destination, arrival date, anddeparture date as arguments and returns flight data containingdetails such as carrier, price, and flight code for the flights. TheLLM will use this tool to find flights to the location once the userhas selected the dates they wish to travel. This tool can either usethe RapidAPI SkyScraper API if you have an API key configured inyour .env file, or it will generate mock data if it's unable to detectthe API key.First, change directories into the tools directory:Then get the tool by running the following command to download itfrom the companion GitHub repository:
Next, familiarize yourself with the tool by reviewing the code. Try toanswer the following questions about the code:What is the purpose of the search_flights function? (It'snot as straightforward of an answer as it may appear)$ cd tools
```
$ curl -o search_flights.py https://raw.githubusercontent.com/temporal-community/tutorial-temporal-ai-agent/main/tools/search_flights.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

How many REST API calls does is it take to call complete thereal flight API search?Once you have finished reviewing the code, you will test it.Create another test within the scripts directory namedsearch_flights_test.py and add the following code:
This test searches for a flight from Chicago to Dallas-Fort Worth.However, since this tool can operate in either a mock mode or liveAPI mode, there are two ways to verify it.Testing the mocked search_flight toolLet's start by testing it without the RapidAPI key. If you have thatset in your .env file, comment it out for now, or skip this step.Change directories back to the root of the project and run the testusing the following command:import jsonfrom tools.search_flights import search_flightsif __name__ == "__main__":    flights = search_flights(        ```
{            "origin": "ORD",            "destination": "DFW",            "dateDepart": "2025-09-20",            "dateReturn": "2025-09-22",        }
```    )    print(json.dumps(flights, indent=2))

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Your output will vary, as the mock data function randomlygenerates results. The output should, however, look something likethis with more items in the results list:
If you aren't planning on using the Sky Scrapper API, you can skipthis next step and continue if you'd like.Testing the Sky Scrapper powered search_flights toolTesting the API-powered version of the tool is similar to testing themocked version.First, if you haven't uncommented the RAPID_API lines in your.env file and added your API key, do this before running the test.You will also need to uncomment the RAPIDAPI_HOST_FLIGHTS$ cd ..uv run scripts/search_flights_test.py
```
```
{  "currency": "USD",  "destination": "DFW",  "origin": "ORD",  "results": [    {      "operating_carrier": "Southwest Airlines",      "outbound_flight_code": "WN427",      "price": 462.43,      "return_flight_code": "WN744",      "return_operating_carrier": "Southwest Airlines"    }
```  ]}

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

environment variable as this is the endpoint the tool will beaccessing.Next, review the code in scripts/search_flights_test.pyand make sure that the dateDepart and dateReturn dates areboth in the future. At this point you have no way of determining ifthe dates are in the past, and the API will return an error if you tryto search for flights in the past.Once you've reviewed the code, make sure you are at the rootdirectory of the project. If are still in the scripts directory, runthe following command:Then run the test using the following command:If you've changed the dates or cities, you may see different results,but the format should be similar to this:RAPIDAPI_KEY=YOUR_RAPID_API_KEYRAPIDAPI_HOST_FLIGHTS=sky-scrapper.p.rapidapi.com
```
$ cd ..$ uv run scripts/search_flights_test.py
```
Searching for: ORDSearching for: DFW```
{  "origin": "ORD",  "destination": "DFW",  "currency": "USD",  "results": [

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

INFOIf the API gives you cryptic error messages such asSomething went wrong or returns an incomplete response,you can try running it a few times and see if you get adifferent response.Now that you have finished testing the search_flights tool, youcan add the final tool to the agent's toolkit.Acquiring the create_invoice toolThe final tool is the create_invoice tool. The tool takes thecustomer's email and trip information such as the cost of the flight,the description of the event, the number of days until the invoice isdue, and generates a sample invoice for that user showing thedetails of the flight and the cost. The LLM will use this tool toinvoice the customer once the customer has confirmed their travelplans. This tool can either use the Stripe API if you have an API keyconfigured in your .env file, or it will generate a mock invoice if itis unable to detect an API key.First, change directories into the tools directory again:    {      "outbound_flight_code": "NK824",      "operating_carrier": "Spirit Airlines",      "return_flight_code": "NK828",      "return_operating_carrier": "Spirit Airlines",      "price": 119.98    }
```,  ]}

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Then get the tool by running the following command to download itfrom the companion GitHub repository:
Next, familiarize yourself with the tool by reviewing the code. Try toanswer the following questions about the code:What customer related verification does the tool do beforecreating the invoice?What does the tool do if this verification fails?Once you have finished reviewing the code, test it.Create another test within the scripts directory namedcreate_invoice_test.py and add the following code:$ cd tools
```
$ curl -o create_invoice.py https://raw.githubusercontent.com/temporal-community/tutorial-temporal-ai-agent/main/tools/create_invoice.py
```
from tools.create_invoice import create_invoiceif __name__ == "__main__":    args_create = ```
{        "email": "ziggy.tardigrade@example.com",        "amount": 150.00,        "description": "Flight to Replay",        "days_until_due": 7,    }
```    invoice_details = create_invoice(args_create)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

However, since this tool can operate in either a mock mode or liveAPI mode, there are two ways to verify it.Testing the mocked create_invoice toolStart by testing it without the Stripe key. If you have it set in your.env file, comment it out for now, or skip this step.Change directories back to the root project directory and run thetest using the following command:The output should be:
If you aren't planning on using the Stripe API, you can skip thisnext step and continue if you'd like.Testing the Stripe-powered create_invoice toolTesting the Stripe powered version of the tool is nearly identical totesting the mocked version of the tool.    print(invoice_details)
```
$ cd ..uv run scripts/create_invoice_test.py[CreateInvoice] Creating invoice with: ```
{'email': 'ziggy.tardigrade@example.com', 'amount': 150.0, 'description': 'Flight to Replay', 'days_until_due': 7}
``````
{'invoiceStatus': 'generated', 'invoiceURL': 'https://pay.example.com/invoice/12345', 'reference': 'INV-12345'}
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

First, if you haven't uncommented the STRIPE_API_KEY lines inyour .env file and added your API key, do this before running thetest.DANGERMake sure you have set up your Stripe account as a sandboxand are using an API key from there. If it is your first timesetting up a Stripe account and you haven't added any billinginformation, this will be the default. Otherwise the invoiceswill be real.Make sure you aren't in the scripts directory any more. If youare, run the following command to get back to the root directory ofthe project:Then run the test using the following command the same way youwould the mocked version:The result will contain an invoiceURL, as well as the status of theinvoice and a reference.STRIPE_API_KEY=YOUR_STRIPE_API_KEY
```
$ cd ..
```
$ uv run scripts/create_invoice_test.py
```
```
{'invoiceStatus': 'open', 'invoiceURL': 'https://invoice.stripe.com/i/acct_1RMFbIQej3CO0i8K/test_YWNjdF8xUk1GYklRZWozQ08wThLLF9TVJpYWZ2WXREVXZrcDJqMGhIM0hSdkVEa2hVYmM0LDE0MTI2NjEwNg0200VaZpBdSc?

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

By following that invoice link in a browser, Stripe will present youwith a sample invoice in your sandbox environment.And those are the three tools in this agent's toolkit to achieve itsgoal. Other goals may have different tools, and you could add moretools. Next, you'll make the tools available to the agent to use.Exposing the tools to theagentNow that you have the tools necessary to complete the agent'sgoal, you need to implement a way to inform the agent that thesetools are available. To do this, you'll create a tool registry. The toolregistry will contain a definition of each tool, along with informationsuch as the tool's name, description, and what arguments itaccepts.However, before you create the registry, you should define the tooldefinition and tool argument as models that can be shared acrossyour codebase.Defining the core modelsDefining the tool arguments, tool definition, and agent goal ascustom types allows for better reusability and type hinting.s=ap', 'reference': 'FEUS4MXS-0001'}
```Before you move on, verify that you have created all thenecessary files in the correct structure.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Temporal also recommends passing a single object betweenfunctions, and requires these objects to be serializable. Giventhese requirements, you'll implement the ToolArgument andToolDefinition types as a Python dataclass.Before you define these models, navigate to the root directory ofyour project and create the models directory:Since this directory will be imported throughout your project, itneeds to be configured as a module. To do this, create a blank__init__.py file by running the following command:Next, create the file core.py. This file will contain the toolargument and definition models used to in your agent. Openmodels/core.py and add the following imports:Next, add the ToolArgument dataclass to the file:$ mkdir models
```
$ touch models/__init__.py
```
from dataclasses import dataclassfrom typing import List@dataclassclass ToolArgument:    name: str    type: str    description: str

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

An instance of this dataclass will represent an argument thatyour tool can accept, including the name of the argument, adescription of what the argument represents, and the type of theargument, such as an int or str.Next, add the ToolDefinition dataclass to the file:
This will hold information about the tool that's provided to theagent so it can determine what action to take. It defines the nameof the tool, a description of what the can do, and an argument list.This list is composed of your ToolArgument objects.Now that you have the appropriate model to define your tools, youcan create a registry of the tools for the agent to access.Creating the tool registryAgents use LLMs to determine what action to take and thenexecute a tool from their toolkit. However, you have to make thosetools available to the agent. Now that you have structure fordefining your tools, you should create a registry that your agentreads to load the available tools.Navigate back to the tools directory and create the filetools/tool_registry.py. In this file you will define all of yourtools using the models you defined in the previous step.@dataclassclass ToolDefinition:    name: str    description: str    arguments: List[ToolArgument]

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

First, add the following import to the file to import the models:Next, add the first part of the ToolDefinition for thefind_events tool:
This defines your tool using the ToolDefinition model youdefined, gives it a name and a description that the LLM can use tounderstand the tool and also use as a prompt. Next you need toadd the arguments to this instantiation. The arguments in theToolDefinition model were defined as aList[ToolArgument], so you may have multiple argumentswithin your list.To complete the definition, add the following code to yourfind_events_tool instantiation to add the arguments:from models.core import ToolArgument, ToolDefinition
find_events_tool = ToolDefinition(    name="FindEvents",    description="Find upcoming events to travel to a given city (e.g., 'New York City') and a date or month. "    "It knows about events in North America only (e.g. major North American cities). "    "It will search 1 month either side of the month provided. "    "Returns a list of events. ",    # arguments to be inserted here in the next step)
    arguments=[

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The find_events tool requires two arguments, the city andmonth in which to search, and it also provides a string descriptionso the LLM would know how to prompt the user if an argument ismissing.Bringing it all together, the complete ToolDefinition would be:    arguments=[        ToolArgument(            name="city",            type="string",            description="Which city to search for events",        ),        ToolArgument(            name="month",            type="string",            description="The month to search for events (will search 1 month either side of the month provided)",        ),    ]
find_events_tool = ToolDefinition(    name="FindEvents",    description="Find upcoming events to travel to a given city (e.g., 'New York City') and a date or month. "    "It knows about events in North America only (e.g. major North American cities). "    "It will search 1 month either side of the month provided. "    "Returns a list of events. ",    arguments=[        ToolArgument(            name="city",            type="string",

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Now that you have the first tool defined in your registry, implementthe remaining tool definitions.Add the following code to register the search_flights tool. Thestructure is similar to the find_events tool, except thatsearch_flights requires more arguments, to search for theorigin, destination, departure date, return date, and confirmationstatus. These arguments are a direct mapping of the requiredparameters to the RAPIDAPI REST API. When creating a tool thatmaps to an API, be sure to include that APIs required parametersas ToolArguments.            description="Which city to search for events",        ),        ToolArgument(            name="month",            type="string",            description="The month to search for events (will search 1 month either side of the month provided)",        ),    ],)
search_flights_tool = ToolDefinition(    name="SearchFlights",    description="Search for return flights from an origin to a destination within a date range (dateDepart, dateReturn). "    "You are allowed to suggest dates from the conversation history, but ALWAYS ask the user if ok.",    arguments=[        ToolArgument(

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

And then add the following code to register the create_invoice            name="origin",            type="string",            description="Airport or city (infer airport code from city and store)",        ),        ToolArgument(            name="destination",            type="string",            description="Airport or city code for arrival (infer airport code from city and store)",        ),        ToolArgument(            name="dateDepart",            type="ISO8601",            description="Start of date range in human readable format, when you want to depart",        ),        ToolArgument(            name="dateReturn",            type="ISO8601",            description="End of date range in human readable format, when you want to return",        ),        ToolArgument(            name="userConfirmation",            type="string",            description="Indication of the user's desire to search flights, and to confirm the details "            + "before moving on to the next step",        ),    ],)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

tool. This tool requires three arguments: the amount to be paid, thedetails of the trip, and a user confirmation.
You now have a tool registry your agent imports to inform it of whattools it has available to execute. Finally, you need to create amapping between the tool registered in tool_registry.py withcreate_invoice_tool = ToolDefinition(    name="CreateInvoice",    description="Generate an invoice for the items described for the total inferred by the conversation history so far. Returns URL to invoice.",    arguments=[        ToolArgument(            name="amount",            type="float",            description="The total cost to be invoiced. Infer this from the conversation history.",        ),        ToolArgument(            name="tripDetails",            type="string",            description="A description of the item details to be invoiced, inferred from the conversation history.",        ),        ToolArgument(            name="userConfirmation",            type="string",            description="Indication of user's desire to create an invoice",        ),    ],)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

the actual functions the Activity will invoke during Workflowexecution.Mapping the registry to the functionsYour agent will use the registry to identify which tool it should use,but it still needs to translate the string name of the tool to thefunction definition the code will execute. You will modify the codein tool_registry to add this functionality.First, add the following imports with the other imports intool_registry.py:
These handle the appropriate typings, as well as import thefunction from each of the tool files.Next, go to the bottom of the file after the previous tool definitionsand add the code to map the string representation of theToolDefinition to the function:from typing import Any, Callable, Dictfrom tools.create_invoice import create_invoicefrom tools.find_events import find_eventsfrom tools.search_flights import search_flights
# Dictionary mapping tool names to their handler functionsTOOL_HANDLERS: Dict[str, Callable[..., Any]] = ```
{    "SearchFlights": search_flights,    "CreateInvoice": create_invoice,    "FindEvents": find_events,}
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Finally, add a function named get_handler that returns thefunction given the tool name:
You have now successfully implemented a structured model forexpressing tools available to your AI agent. This is necessary forbuilding a robust, capable agent.def get_handler(tool_name: str) -> Callable[..., Any]:    """Get the handler function for a given tool name.    Args:        tool_name: The name of the tool to get the handler for.    Returns:        The handler function for the specified tool.    Raises:        ValueError: If the tool name is not found in the registry.    """    if tool_name not in TOOL_HANDLERS:        raise ValueError(f"Unknown tool: ```
{tool_name}
```")    return TOOL_HANDLERS[tool_name]
The tools/tool_registry.py is complete and will needno more revisions. You can review the complete file andcopy the code here.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

In the next step, you will use the tool definitions you just created todefine the agent's goal.Designating the agent'sgoalAn agent's goal is the definition of the task it's trying to achieve. Itachieves this goal by executing tools, analyzing the results, andusing an LLM to decide what to do next. In this tutorial you willdefine the goal as a combination of several fields, including adescription, a starter prompt, an example conversation history, andthe list of tools the agent can use to achieve its goal. Now thatyou've defined the ToolDefinition that will be available for youragent, you can define the AgentGoal type and create youragent's goal.Defining the AgentGoal typeTo define the AgentGoal type, open models/core.py and addthe following code:Before moving on to the next section, verify that your fileand directory structure is correct.
@dataclassclass AgentGoal:    agent_name: str    tools: List[ToolDefinition]    description: str    starter_prompt: str    example_conversation_history: str

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This dataclass defines your AgentGoal as a combination of afew attributes:agent_name - A human readable name for the agenttools - A list of tools, defined as ToolDefinition types,that the agent can use to achieve its goaldescription - A description of the goal, in a bulleted listformat specifying how to achieve it.starter_prompt - A starter prompt for the AI agent to runexample_conversation_history - A sample conversationhistory of what a successful interaction with this agent wouldlook like
Now that you have the type available to define the goal, you willimplement the goal for your agent.Implementing the goal registrySimilar to implementing the tool_registry, next you willimplement a goal_registry to define your agent's goal andmake it available to the Workflow. You will do this by creating aninstance of your AgentGoal type for every goal you wish toimplement. For this tutorial you will only implement a single goal,named goal_event_flight_invoice, but you may want to usethis framework going forward to create your own agent goals at aThe models/core.py is complete and will need no morerevisions. You can review the complete file and copy thecode here.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

later date.To implement your agent's goal, create the filetools/goal_registry.py and add the following imports to thefile:To create the goal, first create an instance of the AgentGoaldataclass and add the first parameter, agent_name, to identifythe goal:
Next, pass in the ToolDefnitions that the agent is allowed touse to accomplish its goal to the tools parameter. Add thefollowing code as the next parameter:
The following parameter defines a detailed description of what thegoal is and the ideal path for the agent to take to achieve its goal.import tools.tool_registry as tool_registryfrom models.core import AgentGoal
goal_event_flight_invoice = AgentGoal(    agent_name="North America Event Flight Booking",    # ...
    # ...    tools=[        tool_registry.find_events_tool,        tool_registry.search_flights_tool,        tool_registry.create_invoice_tool,    ],    # ...

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Add the following code to the file:
The next parameter provides a starter prompt for the agent,detailing how it should begin its interaction with every user. Astarter prompt is the first prompt an agent sees, and gives theinitial set of instructions. Think of this an initialization function forthe conversation. A common format is to provide a greeting,explain your purpose, and prompt the user for information theagent needs to succeed.Add the following code to define your prompt:
Finally, draft an example conversation of a successful interactionwith your agent to pass in. LLMs perform better when they have anexample of expected output, so providing this aids the LLM in itsgoal. Since this is a str type, but the conversation is long, you willdefine each statement as a line in a list and then use 
"\n    # ...    description="Help the user gather args for these tools in order: "    "1. FindEvents: Find an event to travel to "    "2. SearchFlights: search for a flight around the event dates "    "3. CreateInvoice: Create a simple invoice for the cost of that flight ",    # ...
    # ...    starter_prompt="Welcome me, give me a description of what you can do, then ask me for the details you need to do your job.",    # ...

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

".join() to create a string from your conversation. Add theconversation as the final parameter.    # ...    example_conversation_history="\n ".join(        [            "user: I'd like to travel to an event",            "agent: Sure! Let's start by finding an event you'd like to attend. I know about events in North American cities. Could you tell me which city and month you're interested in?",            "user: nyc in may please",            "agent: Great! Let's find an events in New York City in May.",            "user_confirmed_tool_run: <user clicks confirm on FindEvents tool>",            "tool_result: ```
{ 'event_name': 'Frieze New York City', 'event_date': '2023-05-01' }
```",            "agent: Found an event! There's Frieze New York City on May 1 2025, ending on May 14 2025. Would you like to search for flights around these dates?",            "user: Yes, please",            "agent: Let's search for flights around these dates. Could you provide your departure city?",            "user: San Francisco",            "agent: Thanks, searching for flights from San Francisco to New York City around 2023-02-25 to 2023-02-28.",            "user_confirmed_tool_run: <user clicks confirm on SearchFlights tool>"            'tool_result: results including ```
{"flight_number": "AA101", "return_flight_number": "AA102", "price": 850.0}
```',

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Now that you have defined your agent's goal, you can beginimplementing the Activities.Building Temporal Activitiesto execute non-deterministicagent codeNow that you have built the agent's goal, and the tools it needs to            "agent: Found some flights! The cheapest is AA101 for $850. Would you like to generate an invoice for this flight?",            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool>",            'tool_result: ```
{ "status": "success", "invoice": { "flight_number": "AA101", "amount": 850.0 }
```, invoiceURL: "https://example.com/invoice" }',            "agent: Invoice generated! Here's the link: https://example.com/invoice",        ]    ),)The tools/goal_registry.py is complete and will needno more revisions. You can review the complete file andcopy the code here.Before moving on to the next section, verify your files anddirectory structure is correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

achieve it, you can start building the agent code. In this step, youwill create Activities that execute code in your AI agent that canbehave non-deterministically, such as making the LLM calls orcalling tools. Because tools can call out to external services, havethe possibility to fail, be rate limited, or perform other non-deterministic operations, it's safer to always call them in anActivity. When an Activity fails, it's automatically retried by defaultuntil it succeeds or is canceled.Another added benefit of executing your tool as an Activity is thatafter the Activity completes, the result is saved to an Event Historymanaged by Temporal. If your application were to then crash afterexecuting a few tools, it could reconstruct the state of theexecution and use the previous execution's results, without havingto re-execute the tools. This provides durability to your agent forintermittent issues, which are common in distributed systems.Before you can proceed to creating the Activities, however, youneed to create the custom types that you'll use for Activitycommunication. Recall that Workflow and Activity best practicesrecommend only passing a single dataclass parameter. Thishelps with the evolution of parameters as well as ensuring typesafety.Creating the requests data modelsYour agent will require specific types for input and output for boththe Activities and the Workflow. You will put all request-basedmodels in a new file in the models directory named requests.py.First, open models/requests.py and add the following importstatements:

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

You will use these when creating the new types for your agent.Next, add the following single attribute data types to the file:
These types are used to compose other, multi-attributedataclass types, or sent as a single parameter. They are used inthe following context of the agent:Message - A nested dictionary that represents one turn of aconversation between the LLM and the userConversationHistory - A dictionary containing an str keyand a List of Messages that keeps track of theconversation between the LLM and the userNextStep - A Literal containing three options, picked bythe agent to decide the next action to take and interpreted bythe WorkflowCurrentTool - An str representation of the current tool theagent is usingNext, add the following dataclasses for handling the primaryagent parameters:from dataclasses import dataclass, fieldfrom typing import Any, Deque, Dict, List, Literal, Optional, TypedDict, Unionfrom models.core import AgentGoal
Message = Dict[str, Union[str, Dict[str, Any]]]ConversationHistory = Dict[str, List[Message]]NextStep = Literal["confirm", "question", "done"]CurrentTool = str

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The AgentWorkflowParams type contains a summary of theconversation and a queue of prompts that the agent needs toprocess via the LLM. The CombinedInput type contains theagent's goal and the parameters. This type is the input that ispassed to the main agent Workflow and is used to start the initialWorkflow Execution.Next, add the dataclass that handles the input for calling theLLM for tool planning:
ToolPromptInput contains the prompt the Activity will issue tothe LLM, along with any context that the LLM needs whenexecuting the prompt.To go along with the this type, you need to add types that store theresults of validation of the prompt:@dataclassclass AgentGoalWorkflowParams:    conversation_summary: Optional[str] = None    prompt_queue: Optional[Deque[str]] = None@dataclassclass CombinedInput:    agent_goal: AgentGoal    tool_params: AgentGoalWorkflowParams
@dataclassclass ToolPromptInput:    prompt: str    context_instructions: str
@dataclass

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The ValidationInput type contains the prompt given by theuser, the conversation history, and the agent's goal. An Activity willuse this type as input and validate the prompt against the agent'sgoal. Conversely, the ValidationResult type will contain theresults of this validation Activity and will return a boolean signifyingif the prompt passed or failed, and if it did fail a reason why.Next, add two more dataclasses for handling the input andoutput of reading environment variables into the Workflow:
Since reading from the filesystem is a non-deterministic operation,this action must be done from an Activity, so it is best practice to@dataclassclass ValidationInput:    prompt: str    conversation_history: ConversationHistory    agent_goal: AgentGoal@dataclassclass ValidationResult:    validationResult: bool    validationFailedReason: Dict[str, Any] = field(default_factory=dict)
@dataclassclass EnvLookupInput:    show_confirm_env_var_name: str    show_confirm_default: bool@dataclassclass EnvLookupOutput:    show_confirm: bool

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

define types to handle this in case you ever need to add moreenvironment variables. Your environment variables will containthings such as your API keys, agent configurations, timeouts, andother settings.Finally, add the class that will contain the next step the agentshould take and the data the tool needs to execute:
ToolData contains the NextStep that the agent should take,along with the tool that should be used, the arguments for the tool,the response from the LLM, and a force_confirm boolean. Youmay notice this type is different from the previous types, as it is asubclass of TypedDict and not a dataclass. This is done tohandle converting the type to JSON for use in the API later,because dataclasses don't support conversion of nestedcustom types to JSON.
Now that you have your custom types defined for Activitycommunication, you can implement the Activities.Creating the Activities submoduleclass ToolData(TypedDict, total=False):    next: NextStep    tool: str    response: str    args: Dict[str, Any]    force_confirm: bool
The models/requests.py is complete and will need nomore revisions. You can review the complete file and copythe code here.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

First, create the directory structure for your Activities and make it amodule:Next, create the file activities/activities.py and add thenecessary import statements and a statement to load theenvironment variables:
This imports various system packages, Temporal libraries, thelitellm package for making LLM calls, the dotenv package forloading environment variables, and a number of custom types you$ mkdir activitiestouch activities/__init__.py
```
import inspectimport jsonimport osfrom datetime import datetimefrom typing import Sequencefrom dotenv import load_dotenvfrom litellm import completionfrom temporalio import activityfrom temporalio.common import RawValuefrom models.requests import (    EnvLookupInput,    EnvLookupOutput,    ToolPromptInput,    ValidationInput,    ValidationResult,)load_dotenv(override=True)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

defined in models/requests.py. Next, you'll create theAgentActivities class, which contains activities the agent willcall to achieve its goal.Constructing the AgentActivitiesClassThe AgentActivities class enables the Workflow to plan whichtools to use, validate prompts, read in environment variables, andmore.To implement it, open activities/activities.py and createthe class and define the __init__ method:
Temporal Activities can be implemented as either a function or aclass and method. As the agent requires a persistent object forcommunication, in this case, communicating to the LLM, it's goodclass AgentActivities:    def __init__(self):        """Initialize LLM client using LiteLLM."""        self.llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4")        self.llm_key = os.environ.get("LLM_KEY")        self.llm_base_url = os.environ.get("LLM_BASE_URL")        activity.logger.info(            f"Initializing AgentActivities with LLM model: ```
{self.llm_model}
```"        )        if self.llm_base_url:            activity.logger.info(f"Using custom base URL: ```
{self.llm_base_url}
```")

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

practice to use a class and set the parameters as part of theinitialization of the Activity, so to not waste resources re-initializingthe object for every LLM call. The __init__ method reads theLLM configuration from environment variables and assigns thevalues to instance variables.Implementing various helper methodsBefore you implement the Activities, implement the followinghelper functions:The first method sanitizes the JSON response you get from theLLM and sanitizing it to a proper JSON string. The LLM may returna string with extra whitespace, or formatted as markdown, sosanitizing the string is necessary before parsing it.Add the following helper method to the bottom of youractivities.py file:    def sanitize_json_response(self, response_content: str) -> str:        """        Sanitizes the response content to ensure it's valid JSON.        """        # Remove any markdown code block markers        response_content = response_content.replace("```json", "").replace("```", "")        # Remove any leading/trailing whitespace        response_content = response_content.strip()        return response_content

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The second helper function takes a string as input and returns adictionary after attempting to parse the string as valid JSON. Addthis method to the bottom of your activities.py file:
Now that you have the helper methods implemented, you canimplement the Activity responsible for making LLM calls.Implementing the Activity for making LLM callsThe agent_toolPlanner Activity handles all interactions withyour chosen LLM. It makes the call to the LLM, parses theresponse and returns JSON on success, and raises an Exceptionon failure.Add the method header with the appropriate decorator to youractivities.py file, underneath the __init__ method:    def parse_json_response(self, response_content: str) -> dict:        """        Parses the JSON response content and returns it as a dictionary.        """        try:            data = json.loads(response_content)            return data        except json.JSONDecodeError as e:            activity.logger.error(f"Invalid JSON: ```
{e}
```")            raise
    @activity.defn    async def agent_toolPlanner(self, input: ToolPromptInput) -> dict:

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, create the messages list, which contains variousdictionaries with the data necessary to perform an LLM prompt.This format is specifically OpenAI's format, which you can use forany LLM, because you are using LiteLLM to as your LLMabstraction library.Add the following code to craft the messages list:
The agent_toolPlanner Activity constructs standard OpenAI-format messages with system context and user input. Itautomatically includes the current date, which helps the languagemodel provide accurate responses for time-sensitive queries.Continue the method with the LLM call implementation:        messages = [            ```
{                "role": "system",                "content": input.context_instructions                + ". The current date is "                + datetime.now().strftime("%B %d, %Y"),            }
```,            ```
{                "role": "user",                "content": input.prompt,            }
```,        ]
        try:            completion_kwargs = ```
{                "model": self.llm_model,                "messages": messages,

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This call is wrapped in a try/except statement to handle apotential failure. It creates a dictionary containing the argumentsfor calling the LLM, including the model choice, the messages, theAPI key, and a custom base URL if set. Next it performs the call tothe LLM using the completion function, passing in thearguments dictionary. It then extracts the message you want fromthe response content, sanitizes the JSON and returns it asproperly parsed JSON upon success. Upon failure, it will raise anexception.                "api_key": self.llm_key,            }
```            # Add base_url if configured            if self.llm_base_url:                completion_kwargs["base_url"] = self.llm_base_url            response = completion(**completion_kwargs)            response_content = response.choices[0].message.content            activity.logger.info(f"LLM response: ```
{response_content}
```")            # Use the new sanitize function            response_content = self.sanitize_json_response(response_content)            return self.parse_json_response(response_content)        except Exception as e:            activity.logger.error(f"Error in LLM completion: ```
{str(e)}
```")            raise

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The complete implementation of agent_toolPlanner is asfollows:    @activity.defn    async def agent_toolPlanner(self, input: ToolPromptInput) -> dict:        messages = [            ```
{                "role": "system",                "content": input.context_instructions                + ". The current date is "                + datetime.now().strftime("%B %d, %Y"),            }
```,            ```
{                "role": "user",                "content": input.prompt,            }
```,        ]        try:            completion_kwargs = ```
{                "model": self.llm_model,                "messages": messages,                "api_key": self.llm_key,            }
```            # Add base_url if configured            if self.llm_base_url:                completion_kwargs["base_url"] = self.llm_base_url            response = completion(**completion_kwargs)            response_content = 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Now that you have implemented the Activity to call the LLM, youwill implement the Activity to validate the user's prompts.Implementing the Activity for prompt validationIt is important to not let the user take your agent off on a tangent,sending prompts that are not related to the goal. To do this, youmust validate the prompt against your agent's goal and contextprior to executing the LLM with the user's input.Next, create the agent_validatePrompt Activity to validate anyprompt sent to the LLM in the context of the conversation historyand agent goal.Within the AgentActivities class, add the following methodheader:response.choices[0].message.content            activity.logger.info(f"LLM response: ```
{response_content}
```")            # Use the new sanitize function            response_content = self.sanitize_json_response(response_content)            return self.parse_json_response(response_content)        except Exception as e:            activity.logger.error(f"Error in LLM completion: ```
{str(e)}
```")            raise
    @activity.defn    async def agent_validatePrompt(        self, validation_input: ValidationInput

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This Activity takes in a single argument, using the customValidationInput type you specified, and returns a single value,ValidationResult, in accordance with Temporal best practices.Next, add the code following code to iterate over the toolsspecified in the agent's goal and add them to a list.
By doing this, you are creating a string the LLM can use as contextto validate against. This context helps the LLM understand whatcapabilities are available to the agent, and whether or not theprompt the user sent makes sense.    ) -> ValidationResult:        """        Validates the prompt in the context of the conversation history and agent goal.        Returns a ValidationResult indicating if the prompt makes sense given the context.        """
        # Create simple context string describing tools and goals        tools_description = []        for tool in validation_input.agent_goal.tools:            tool_str = f"Tool: ```
{tool.name}
```\n"            tool_str += f"Description: ```
{tool.description}
```\n"            tool_str += "Arguments: " + ", ".join(                [f"```
{arg.name}
``` (```
{arg.type}
```)" for arg in tool.arguments]            )            tools_description.append(tool_str)        tools_str = "\n".join(tools_description)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Continue the validation method by adding conversation context:
This section gathers the past conversation history andconcatenates it with the available tool context, creating a completecontext for the LLM.Next, add the following prompt for the LLM to use to validate theprompt:        # Convert conversation history to string        history_str = json.dumps(validation_input.conversation_history, indent=2)        # Create context instructions        context_instructions = f"""The agent goal and tools are as follows:            Description: ```
{validation_input.agent_goal.description}
```            Available Tools:            ```
{tools_str}
```            The conversation history to date is:            ```
{history_str}
```"""
        # Create validation prompt        validation_prompt = f"""The user's prompt is: "```
{validation_input.prompt}
```"            Please validate if this prompt makes sense given the agent goal and conversation history.            If the prompt makes sense toward the goal then validationResult should be true.            If the prompt is wildly nonsensical or makes no sense toward the goal and current conversation history then validationResult should be false.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Finally, instantiate a ToolPromptInput object and pass that toagent_toolPlanner to execute:            If the response is low content such as "yes" or "that's right" then the user is probably responding to a previous prompt.               Therefore examine it in the context of the conversation history to determine if it makes sense and return true if it makes sense.            Return ONLY a JSON object with the following structure:                "validationResult": true/false,                "validationFailedReason": "If validationResult is false, provide a clear explanation to the user in the response field                 about why their request doesn't make sense in the context and what information they should provide instead.                validationFailedReason should contain JSON in the format                ```
{{                    "next": "question",                    "response": "[your reason here and a response to get the user back on track with the agent goal]"                }
```}                If validationResult is true (the prompt makes sense), return an empty dict as its value ```
{{}
```}"            """
        # Call the LLM with the validation prompt        prompt_input = ToolPromptInput(            prompt=validation_prompt, context_instructions=context_instructions        )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The complete implementation of agent_validatePrompt is asfollows:        result = await self.agent_toolPlanner(prompt_input)        return ValidationResult(            validationResult=result.get("validationResult", False),            validationFailedReason=result.get("validationFailedReason", ```
{}
```),        )
@activity.defn    async def agent_validatePrompt(        self, validation_input: ValidationInput    ) -> ValidationResult:        """        Validates the prompt in the context of the conversation history and agent goal.        Returns a ValidationResult indicating if the prompt makes sense given the context.        """        # Create simple context string describing tools and goals        tools_description = []        for tool in validation_input.agent_goal.tools:            tool_str = f"Tool: ```
{tool.name}
```\n"            tool_str += f"Description: ```
{tool.description}
```\n"            tool_str += "Arguments: " + ", ".join(                [f"```
{arg.name}
``` (```
{arg.type}
```)" for arg in tool.arguments]            )            tools_description.append(tool_str)        tools_str = "\n".join(tools_description)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

        # Convert conversation history to string        history_str = json.dumps(validation_input.conversation_history, indent=2)        # Create context instructions        context_instructions = f"""The agent goal and tools are as follows:            Description: ```
{validation_input.agent_goal.description}
```            Available Tools:            ```
{tools_str}
```            The conversation history to date is:            ```
{history_str}
```"""        # Create validation prompt        validation_prompt = f"""The user's prompt is: "```
{validation_input.prompt}
```"            Please validate if this prompt makes sense given the agent goal and conversation history.            If the prompt makes sense toward the goal then validationResult should be true.            If the prompt is wildly nonsensical or makes no sense toward the goal and current conversation history then validationResult should be false.            If the response is low content such as "yes" or "that's right" then the user is probably responding to a previous prompt.               Therefore examine it in the context of the conversation history to determine if it makes sense and return true if it makes sense.            Return ONLY a JSON object with the following structure:                "validationResult": true/false,                "validationFailedReason": "If validationResult is false, provide a clear explanation to the user in the response field                 about why their request doesn't make sense in the context and what information they should provide 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Calling an Activity within another Activity won't invoke that Activity,but will call the method like a typical Python method. The Activitythen returns a ValidationResult for the agent to interpret andcontinue with its execution.Implementing the Activity for retrieving environmentvariablesinstead.                validationFailedReason should contain JSON in the format                ```
{{                    "next": "question",                    "response": "[your reason here and a response to get the user back on track with the agent goal]"                }
```}                If validationResult is true (the prompt makes sense), return an empty dict as its value ```
{{}
```}"            """        # Call the LLM with the validation prompt        prompt_input = ToolPromptInput(            prompt=validation_prompt, context_instructions=context_instructions        )        result = await self.agent_toolPlanner(prompt_input)        return ValidationResult(            validationResult=result.get("validationResult", False),            validationFailedReason=result.get("validationFailedReason", ```
{}
```),        )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The final Activity within the AgentActivities class is theget_wf_env_vars Activity. This Activity reads certainenvironment variables that need to be known within the Workflow.Since reading from the file system is a potentially non-deterministic operation, this must happen within an Activity.Add the following code within the AgentActivities class toimplement the Activity:
This Activity reads the environment variables and ensures that    @activity.defn    async def get_wf_env_vars(self, input: EnvLookupInput) -> EnvLookupOutput:        """gets env vars for workflow as an activity result so it's deterministic        handles default/None        """        output: EnvLookupOutput = EnvLookupOutput(            show_confirm=input.show_confirm_default        )        show_confirm_value = os.getenv(input.show_confirm_env_var_name)        if show_confirm_value is None:            output.show_confirm = input.show_confirm_default        elif show_confirm_value is not None and show_confirm_value.lower() == "false":            output.show_confirm = False        else:            output.show_confirm = True        return output

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

show_confirm_value is set, returning your customEnvLookupOutput type. While this type may only contain onevalue at the moment, having it designed with this custom typeallows you to expand this method later if necessary.You have implemented all Activities within the AgentActivitiesclass, but there is still one Activity left to implement, the Activityfor executing the tools.Implementing dynamic tool executionThe final Activity enables runtime execution of any tool from yourregistry. To enable this, you must use Dynamic Activities, which arenecessary when you request execution of an Activity with anunknown Activity Type. Since your tools are loaded in dynamically,this is a perfect example of when to use Temporal's DynamicActivities.This Activity will not be implemented as a method within the class,but rather a function within the same activities.py file.Add this function outside the class definition:@activity.defn(dynamic=True)async def dynamic_tool_activity(args: Sequence[RawValue]) -> dict:    from tools.tool_registry import get_handler    tool_name = activity.info().activity_type  # e.g. "FindEvents"    tool_args = activity.payload_converter().from_payload(args[0].payload, dict)    activity.logger.info(f"Running dynamic tool 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This dynamic Activity uses Temporal's runtime information todetermine which tool to execute. It retrieves the tool name fromthe Activity type and loads arguments from the payload. It theninspects the handler to determine if the implementation of the toolis an asynchronous Python function. If it is, it awaits itsexecution, otherwise it directly invokes the function. This meansthe Activity handles both synchronous and asynchronous toolfunctions.
The Activities you implemented handle LLM communication, userinput validation, environment configuration, and dynamic toolexecution.'```
{tool_name}
```' with args: ```
{tool_args}
```")    # Delegate to the relevant function    handler = get_handler(tool_name)    if inspect.iscoroutinefunction(handler):        result = await handler(tool_args)    else:        result = handler(tool_args)    # Optionally log or augment the result    activity.logger.info(f"Tool '```
{tool_name}
```' result: ```
{result}
```")    return result
The activities/activities.py is complete and willneed no more revisions. You can review the complete fileand copy the code here.
Before moving on to the next section, verify your files anddirectory structure is correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

In the next step, you will create a submodule that stores andrenders the main prompts the agent uses to communicate with theLLM.Developing the necessarypromptsYour agent communicates with an LLM to determine what steps itshould take and which tool it should use. However, LLM output isnon-determinstic, so how do you ensure that you receive data thatyou can rely on so your agent can interpret it and continueexecution? To do this, you need to carefully craft a promptexplicitly stating what the LLM should do and what format it shouldreturn. These prompts can often be complex, and since your agentdynamically loads tools, will also need to be dynamicallygenerated. In this section, you will implement the code to generatethese prompts.Creating the submoduleFirst, create a new directory named prompts:Then create the __init__.py file in the prompts director tomake it a submodule:mkdir prompts
touch prompts/__init__.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, you'll craft your prompt templates that the LLM will use.Crafting the prompts templatesThe prompts templates you create will vary in the amount ofcustomization they allow. For templates with minimalcustomization, for example, templates that only require a fewvariable substitutions, Python's string formatting syntax willsuffice. However, if your template requires iteration, conditionallogic, or variable interpolation, you should use a more advancedtemplating system, such as Jinja2.Defining the primary context promptThe primary context that the LLM uses to determine the nextaction requires multiple steps, conditionals, and loops toimplement, so you will implement it using Jinja2.Create the file prompts/prompts.py and add the import forJinja2:Next, add the first part of the primary prompt, which you'll nameGENAI_PROMPT:from jinja2 import Template
GENAI_PROMPT = Template(    """You are an AI agent that helps fill required arguments for the tools described below. You must respond with valid JSON ONLY, using the schema provided in the instructions.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This section of the prompt sets the primary role for the LLM,provides the current conversation history for the LLM to analyze,and if an example conversation was provided, provides that as anexample for the LLM to use as well.Continue adding this prompt by adding the following lines:=== Conversation History ===This is the ongoing history to determine which tool and arguments to gather:*BEGIN CONVERSATION HISTORY*```
{{ conversation_history_json }
```}*END CONVERSATION HISTORY*REMINDER: You can use the conversation history to infer arguments for the tools.```
{% if agent_goal.example_conversation_history %}
```=== Example Conversation With These Tools ===Use this example to understand how tools are invoked and arguments are gathered.BEGIN EXAMPLE```
{{ agent_goal.example_conversation_history }
```}END EXAMPLE```
{% endif %}
```"""
"""=== Tools Definitions ===There are ```
{{ agent_goal.tools|length }
```} available tools:```
{{ agent_goal.tools|map(attribute='name')|join(', ') }
```}Goal: ```
{{ agent_goal.description }
```}Gather the necessary information for each tool in the sequence described above.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The segment of the prompt definitions section lists the agent'sgoal and the available tools with their descriptions and argumentspecifications. This provides the LLM with information about whatthe agent is attempting to accomplish, and its capabilities andconstraints.Next, it's vital that the LLM provides its response in a consistentway that your agent can parse. Add the following instructions foroutput formatting and guardrails:Only ask for arguments listed below. Do not add extra arguments.```
{% for tool in agent_goal.tools %}
```Tool name: ```
{{ tool.name }
```}  Description: ```
{{ tool.description }
```}  Required args:```
{% for arg in tool.arguments %}
```    - ```
{{ arg.name }
```} (```
{{ arg.type }
```}): ```
{{ arg.description }
```}```
{% endfor %}
``````
{% endfor %}
```When all required args for a tool are known, you can propose next='confirm' to run it."""
"""=== Instructions for JSON Generation ===Your JSON format must be:```
{  "response": "<plain text>",  "next": "<question|confirm|pick-new-goal|done>",  "tool": "<tool_name or null>",  "args": {

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

    "<arg1>": "<value1 or null>",    "<arg2>": "<value2 or null>",    ...  }
```}1) If any required argument is missing, set next='question' and ask the user.2) If all required arguments are known, set next='confirm' and specify the tool.   The user will confirm before the tool is run.3) ```
{{ toolchain_complete_guidance }
```}4) response should be short and user-friendly.Guardrails (always remember!)1) If any required argument is missing, set next='question' and ask the user.2) ALWAYS ask a question in your response if next='question'.3) ALWAYS set next='confirm' if you have arguments And respond with "let's proceed with <tool> (and any other useful info)"  DON'T set next='confirm' if you have a question to ask.EXAMPLE: If you have a question to ask, set next='question' and ask the user.4) You can carry over arguments from one tool to another. EXAMPLE: If you asked for an account ID, then use the conversation history to infer that argument going forward.5) If ListAgents in the conversation history is force_confirm='False', you MUST check if the current tool contains userConfirmation. If it does, please ask the user to confirm details with the user. userConfirmation overrides force_confirm='False'.EXAMPLE: (force_confirm='False' AND 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This segment provides strict rules on the exact format the LLMshould respond with, as well as guardrails to ensure that fields areset properly. The guardrails section is particularly important as itprovides detailed behavioral constraints that enable consistentresponses. These rules prevent issues such as asking questionswhile proposing tool execution or forgetting to use theconversation history for argument inference.Finally, complete the template with a validation prompt:userConfirmation exists on tool) Would you like me to <run tool> with the following details: <details>?"""
"""```
{% if raw_json is not none %}
```=== Validation Task ===Validate and correct the following JSON if needed:```
{{ raw_json_str }
```}Check syntax, 'tool' validity, 'args' completeness, and set 'next' appropriately. Return ONLY corrected JSON.```
{% endif %}
``````
{% if raw_json is not none %}
```Begin by validating the provided JSON if necessary.```
{% else %}
```Begin by producing a valid JSON response for the next tool or question.```
{% endif %}
```""".strip()

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The validation section enables the template to handle both correctand incorrectly JSON formatted strings. If the JSON is improperlyformatted, the LLM is prompted to correct it before continuing withits other tasks.All together, the template should look like this:)
GENAI_PROMPT = Template(    """You are an AI agent that helps fill required arguments for the tools described below. You must respond with valid JSON ONLY, using the schema provided in the instructions.=== Conversation History ===This is the ongoing history to determine which tool and arguments to gather:*BEGIN CONVERSATION HISTORY*```
{{ conversation_history_json }
```}*END CONVERSATION HISTORY*REMINDER: You can use the conversation history to infer arguments for the tools.```
{% if agent_goal.example_conversation_history %}
```=== Example Conversation With These Tools ===Use this example to understand how tools are invoked and arguments are gathered.BEGIN EXAMPLE```
{{ agent_goal.example_conversation_history }
```}END EXAMPLE```
{% endif %}
```=== Tools Definitions ===There are ```
{{ agent_goal.tools|length }
```} available 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

tools:```
{{ agent_goal.tools|map(attribute='name')|join(', ') }
```}Goal: ```
{{ agent_goal.description }
```}Gather the necessary information for each tool in the sequence described above.Only ask for arguments listed below. Do not add extra arguments.```
{% for tool in agent_goal.tools %}
```Tool name: ```
{{ tool.name }
```}  Description: ```
{{ tool.description }
```}  Required args:```
{% for arg in tool.arguments %}
```    - ```
{{ arg.name }
```} (```
{{ arg.type }
```}): ```
{{ arg.description }
```}```
{% endfor %}
``````
{% endfor %}
```When all required args for a tool are known, you can propose next='confirm' to run it.=== Instructions for JSON Generation ===Your JSON format must be:```
{  "response": "<plain text>",  "next": "<question|confirm|done>",  "tool": "<tool_name or null>",  "args": {    "<arg1>": "<value1 or null>",    "<arg2>": "<value2 or null>",    ...  }
```}1) If any required argument is missing, set next='question' and ask the user.2) If all required arguments are known, set next='confirm' and specify the tool.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

   The user will confirm before the tool is run.3) ```
{{ toolchain_complete_guidance }
```}4) response should be short and user-friendly.Guardrails (always remember!)1) If any required argument is missing, set next='question' and ask the user.2) ALWAYS ask a question in your response if next='question'.3) ALWAYS set next='confirm' if you have arguments And respond with "let's proceed with <tool> (and any other useful info)"  DON'T set next='confirm' if you have a question to ask.EXAMPLE: If you have a question to ask, set next='question' and ask the user.4) You can carry over arguments from one tool to another. EXAMPLE: If you asked for an account ID, then use the conversation history to infer that argument going forward.5) If ListAgents in the conversation history is force_confirm='False', you MUST check if the current tool contains userConfirmation. If it does, please ask the user to confirm details with the user. userConfirmation overrides force_confirm='False'.EXAMPLE: (force_confirm='False' AND userConfirmation exists on tool) Would you like me to <run tool> with the following details: <details>?```
{% if raw_json is not none %}
```=== Validation Task ===Validate and correct the following JSON if needed:

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, you'll create the prompt that will determine the next steps foryour agent to take.Defining the tool completion promptThe TOOL_COMPLETION_PROMPT instructs the LLM to analyze thesuccessful tool results and determine the appropriate next steps.This prompt only requires minimal substitution, so a Python stringformatting will suffice.Add the following constant to your prompts/prompts.py file:```
{{ raw_json_str }
```}Check syntax, 'tool' validity, 'args' completeness, and set 'next' appropriately. Return ONLY corrected JSON.```
{% endif %}
``````
{% if raw_json is not none %}
```Begin by validating the provided JSON if necessary.```
{% else %}
```Begin by producing a valid JSON response for the next tool or question.```
{% endif %}
```""".strip())
TOOL_COMPLETION_PROMPT = """### The '```
{current_tool}
```' tool completed successfully with ```
{dynamic_result}
```. INSTRUCTIONS: Parse this tool result as plain text, and use the system prompt containing the list of tools in sequence and the conversation history (and 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This template handles successful tool completion scenarios,instructing the LLM to use the results of the execution whendetermining the next step. It also gives explicit instructions onexactly how to respond, which keys should be present, and theformat of the output.Next, you'll implement the prompt for handling missing userarguments.Defining the missing arguments promptIf the user doesn't provide enough information to the agent, theagent needs to detect this and set the next action to prompt theuser for the missing arguments. This prompt only has a fewvariable substitutions, so a Python string formatting will suffice.Add the missing arguments template to yourprompts/prompts.py file:previous tool_results) to figure out next steps, if any. You will need to use the tool_results to auto-fill arguments for subsequent tools and also to figure out if all tools have been run. ```
{{"next": "<question|confirm|pick-new-goal|done>", "tool": "<tool_name or null>", "args": {{"<arg1>": "<value1 or null>", "<arg2>": "<value2 or null>"}
```}, "response": "<plain text (can include \\n line breaks)>"}}ONLY return those json keys (next, tool, args, response), nothing else. Next should be "question" if the tool is not the last one in the sequence. Next should be "done" if the user is asking to be done with the chat."""

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This template provides the response, sets the next key toquestion to instruct the agent to prompt the user for moreinformation, and specifies which tool is missing which argument.Defining the toolchain complete promptFinally, define the prompt that details what the LLM should do if nomore tools are needed to complete the agent's goal.
Next, you'll build the functions that use these prompt templates togenerate the actual prompts.Building the prompt generationfunctionsMISSING_ARGS_PROMPT = """### INSTRUCTIONS set next='question', combine this response response='```
{response}
```' and following missing arguments for tool ```
{current_tool}
```: ```
{missing_args}
```. Only provide a valid JSON response without any comments or metadata."""
TOOLCHAIN_COMPLETE_GUIDANCE_PROMPT = "If no more tools are needed (user_confirmed_tool_run has been run for all), set next='done' and tool=''."The prompts/prompts.py is complete and will need nomore revisions. You can review the complete file and copythe code here.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Now that you have the prompt templates built, you need toimplement functions the agent can call to render them.First, create prompts/agent_prompt_generators.py and addthe following imports:
Next, create the function to render the GENAI_PROMPT:import jsonfrom typing import Optionalfrom models.core import AgentGoalfrom models.requests import ConversationHistory, ToolDatafrom prompts.prompts import (    GENAI_PROMPT,    MISSING_ARGS_PROMPT,    TOOL_COMPLETION_PROMPT,    TOOLCHAIN_COMPLETE_GUIDANCE_PROMPT,)def generate_genai_prompt(    agent_goal: AgentGoal,    conversation_history: ConversationHistory,    raw_json: Optional[ToolData] = None,) -> str:    """    Generates a concise prompt for producing or validating JSON instructions    with the provided tools and conversation history.    """    # Prepare template variables    template_vars = ```
{

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This function creates the template_vars dictionary, assigns theparameters to the appropriate template variables, and then rendersthe Jinja2 template, passing in the dictionary as kwargs to therender function.Next, add the tool completion prompt generator:        "agent_goal": agent_goal,        "conversation_history_json": json.dumps(conversation_history, indent=2),        "toolchain_complete_guidance": TOOLCHAIN_COMPLETE_GUIDANCE_PROMPT,        "raw_json": raw_json,        "raw_json_str": (            json.dumps(raw_json, indent=2) if raw_json is not None else None        ),    }
```    return GENAI_PROMPT.render(**template_vars)
def generate_tool_completion_prompt(current_tool: str, dynamic_result: dict) -> str:    """    Generates a prompt for handling tool completion and determining next steps.    Args:        current_tool: The name of the tool that just completed        dynamic_result: The result data from the tool execution    Returns:        str: A formatted prompt string for the agent to process the tool completion

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This function takes in the current tool, along with the dynamicresult system prompt and returns the formattedTOOL_COMPLETION_PROMPT using the .format function.Finally, add the prompt for handling missing arguments:    """    return TOOL_COMPLETION_PROMPT.format(        current_tool=current_tool, dynamic_result=dynamic_result    )
def generate_missing_args_prompt(    current_tool: str, tool_data: dict, missing_args: list[str]) -> str:    """    Generates a prompt for handling missing arguments for a tool.    Args:        current_tool: The name of the tool that needs arguments        tool_data: The current tool data containing the response        missing_args: List of argument names that are missing    Returns:        str: A formatted prompt string for requesting missing arguments    """    return MISSING_ARGS_PROMPT.format(        response=tool_data.get("response"),        current_tool=current_tool,        missing_args=missing_args,

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This function gets the response from the current tool, and thearguments missing, then returns a the formattedMISSING_ARGS_PROMPT.
Now that you have the prompt rendering submodule implemented,you can implement the main agent Workflow.Building the agentWorkflowAgents need to manage conversations that involve multiple turnsincluding user interaction, tool execution, and state management.The challenge is maintaining coherence across these sessionswhile handling failures, retries, and long-running interactions. Youragent must coordinate several concurrent concerns such asvalidating user input against conversation context, determiningwhen to execute tools, managing user input for tool execution, andmaintaining conversation history that persists in the event ofsystem failures. A traditional application would lose conversationstate during failures, but Temporal Workflows provide durable    )
The prompts/agent_prompt_generators.py iscomplete and will need no more revisions. You can reviewthe complete file and copy the code here.Before moving on to the next section, verify your files anddirectory structure is correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

execution that preserves context through any system interruption.In this step, you will create the Temporal Workflow thatorchestrates your agent's conversation loop. This Workflowhandles user interactions, validates prompts, manages toolexecution, and maintains conversation state, all while providingdurability to the agent.Creating the workflows submoduleFirst, create the directory structure for your Workflowimplementations:Next, create an empty __init__.py file in the directory to enableit as a submodule:Now that your workflows directory is a submodule, you willcreate a few helper functions for your Workflow.Implementing a few Workflow helperfunctionsBefore implementing the Workflow, you will implement a few helperfunctions that perform repetitive operations like tool execution,argument validation, and conversation continuation.First, create workflows/workflow_helpers.py and add the$ mkdir workflows
```
$ touch workflows/__init__.py
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

following import statements:
Like previous import statements, this section includes librariesfrom the Python standard library and Temporal libraries. However,there are also libraries being imported with the 
with
workflow.unsafe.imports_passed_through() statement.This statement is necessary when importing third-party libraries,including ones you implement, into a Workflow (or in this case,imported into a file that will be imported by the Workflow). This isdone for performance and determinism safety reasons, which youcan read more about in the Temporal documentation.Next, declare the following timeout constants:from datetime import timedeltafrom typing import Any, Callable, Deque, Dictfrom temporalio import workflowfrom temporalio.common import RetryPolicyfrom temporalio.exceptions import ActivityErrorwith workflow.unsafe.imports_passed_through():    from activities.activities import AgentActivities    from models.requests import ConversationHistory, ToolData, ToolPromptInput    from prompts.agent_prompt_generators import (        generate_missing_args_prompt,        generate_tool_completion_prompt,    )
TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=30)TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

These timeout constants set sensible limits for tool execution andLLM calls, ensuring the calls have enough time to respond, but thatthe Workflow detects a failure within a reasonable amount of time.Defining the tool execution Activity invocation functionThe first function you'll implement is thehandle_tool_execution function. Add the method header tothe file:
This function takes in the current tool to execute, the tool data, acallback that stores the conversation history, and a queue forprompts that the agent will execute later to continue its goal. Thefunction executes the tool as a dynamic Activity, and processesthe results for the LLM to handle.Add the code to invoke the Activity and process the results:timedelta(minutes=30)LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=30)LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = timedelta(minutes=30)
async def handle_tool_execution(    current_tool: str,    tool_data: ToolData,    add_message_callback: Callable[..., Any],    prompt_queue: Deque[str],) -> None:
    """Execute a tool after confirmation and handle its result."""    workflow.logger.info(f"Confirmed. Proceeding with tool: ```
{current_tool}
```")

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

It executes the tool by calling the name of the tool, which getshandled by the dynamic Activity you implemented. When callingthe Activity, you specify the Activity timeouts using the constantsyou defined earlier. Whether the Activity succeeds or fails, theresult is stored to the conversation history using theadd_message_callback that was passed in. Then, the methodinvokes the generate_tool_completion_prompt function withthe current_tool and result of the tool execution to create aprompt and add it to the prompt_queue, which the agent willhandle on its next iteration.Defining the missing argument handler function    try:        dynamic_result = await workflow.execute_activity(            current_tool,            tool_data["args"],            schedule_to_close_timeout=TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,            start_to_close_timeout=TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT,            retry_policy=RetryPolicy(                initial_interval=timedelta(seconds=5), backoff_coefficient=1            ),        )        dynamic_result["tool"] = current_tool    except ActivityError as e:        workflow.logger.error(f"Tool execution failed: ```
{str(e)}
```")        dynamic_result = ```
{"error": str(e), "tool": current_tool}
```    add_message_callback("tool_result", dynamic_result)    prompt_queue.append(generate_tool_completion_prompt(current_tool, dynamic_result))

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next you'll create the function that checks and handles missingtool arguments. Add the function header with the followingarguments:
This function takes in the current_tool, the args that werepassed to the tool, the tool_data containing all data related tothe tool, and the prompt_queue containing prompts the LLM stillneeds to act on.Add the remaining code to check for any missing arguments:async def handle_missing_args(    current_tool: str,    args: Dict[str, Any],    tool_data: Dict[str, Any],    prompt_queue: Deque[str],) -> bool:
    """Check for missing arguments and handle them if found."""    missing_args = [key for key, value in args.items() if value is None]    if missing_args:        prompt_queue.append(            generate_missing_args_prompt(current_tool, tool_data, missing_args)        )        workflow.logger.info(            f"Missing arguments for tool: ```
{current_tool}
```: ```
{' '.join(missing_args)}
```"        )        return True    return False

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The tool arguments are checked, and if any are missing, thegenerate_missing_args_prompt is invoked and the result isadded to the prompt_queue for the agent to execute on its nextturn. The function then returns True. Otherwise, no argumentswere missing and the function returns False.Defining the history formatting functionNext you'll define functions for formatting the conversation history.Add the following function to your code:
This function compacts responses from every message in theconversation history and returns it as a single string.Defining the history summarization prompt functionNow you'll use the previous function to generate a prompt for theLLM to summarize the conversation.Add the following function to your code:def format_history(conversation_history: ConversationHistory) -> str:    """Format the conversation history into a single string."""    return " ".join(str(msg["response"]) for msg in conversation_history["messages"])
def prompt_summary_with_history(    conversation_history: ConversationHistory,) -> tuple[str, str]:    """Generate a prompt for summarizing the 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The code calls the format_history function, then creates twovariables, one containing the history and another containing theprompt. It then returns both variables as a tuple.Defining the function to handle long Event HistoriesTemporal Workflows have a limit on the length and size of a singleWorkflow Execution's Event History. A Temporal Workflow willContinue-As-New when the Event History reaches this limits, andwill continue the execution in a new Workflow Execution, which inturn creates new Event History. Due to the length of LLMresponses, you will implement a function to determine if aContinue-As-New is needed.First, define the function header:conversation.    Used only for continue as new of the workflow."""    history_string = format_history(conversation_history)    context_instructions = f"Here is the conversation history between a user and a chatbot: ```
{history_string}
```"    actual_prompt = (        "Please produce a two sentence summary of this conversation. "        'Put the summary in the format ```
{ "summary": "<plain text>" }
```'    )    return (context_instructions, actual_prompt)
async def continue_as_new_if_needed(    conversation_history: ConversationHistory,    prompt_queue: Deque[str],

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The function receives the conversation_history as yourcustom type, the prompt_queue as the pass-by-object Dequeused to control the flow of prompts, the agent's goal, how manyturns the conversation should last for, and a function callback toadd this interaction to the conversation history.Next, add the function implementation:    agent_goal: Any,    max_turns: int,    add_message_callback: Callable[..., Any],) -> None:
    """Handle workflow continuation if message limit is reached."""    if len(conversation_history["messages"]) >= max_turns:        summary_context, summary_prompt = prompt_summary_with_history(            conversation_history        )        summary_input = ToolPromptInput(            prompt=summary_prompt, context_instructions=summary_context        )        conversation_summary = await workflow.start_activity_method(            AgentActivities.agent_toolPlanner,            summary_input,            schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,        )        workflow.logger.info(f"Continuing as new after ```
{max_turns}
``` turns.")        add_message_callback("conversation_summary", conversation_summary)        workflow.continue_as_new(

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The function first checks if the conversation history's length isgreater than or equal to the maximum number of turns specified. Ifthis evaluates to true, the function proceeds with its 
Continue-
As-New process. First it calls prompt_summary_with_historyto create a summary and prompt context using the current history.It then uses this output to create an input type,ToolPromptInput, based off of this summary for the agent toprocess. Next it calls the agent_toolPlanner Activity with thisinput to invoke the LLM with this summarized context. It then callsthe add_message_callback function, which adds this event tothe conversation history. Finally, it invokesworkflow.continue_as_new to perform the Continue-As-Newoperation, which results in a new Workflow Execution starting atthis point in the Event History, and the current Workflow Executionclosing.Defining the prompt entity identification functionFinally, add a function that returns a boolean it the prompt camefrom a user or not:            args=[                ```
{                    "tool_params": {                        "conversation_summary": conversation_summary,                        "prompt_queue": prompt_queue,                    }
```,                    "agent_goal": agent_goal,                }            ]        )
# LLM-tagged prompts start with "###"

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

LLM prompts start with ###, so any prompt that doesn't beginwith that character sequence is a user prompt.
Now that you have built out the supporting functions, you can buildthe agent Workflow.Preparing the core agent WorkflowThe core agent Workflow is the primary driver of your agent. Itorchestrates LLM and tool execution, maintains conversation state,and makes decisions about what step to take next. The Workflowwill consist of the primary Workflow class and method, as well as afew Signals, Queries, and class methods.First, create workflows/agent_goal_workflow.py, and add thenecessary imports:# all others are from the userdef is_user_prompt(prompt) -> bool:    if prompt.startswith("###"):        return False    else:        return TrueThe workflows/workflow_helpers.py is complete andwill need no more revisions. You can review the completefile and copy the code here.
from collections import dequefrom datetime import timedeltafrom typing import Any, Deque, Dict, Optional, Union

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

These imports bring in the necessary types, helper functions, andconstants you have defined so far, as well as libraries from theTemporal and Python standard library. You also added theMAX_TURNS_BEFORE_CONTINUE constant, and set the value to250. The agent will use this value with thecontinue_as_new_if_needed helper function you implementedto decide if it should Continue-As-New. For the sake of thisfrom temporalio import workflowfrom temporalio.common import RetryPolicyfrom models.core import AgentGoalfrom models.requests import (    ConversationHistory,    CurrentTool,    EnvLookupInput,    EnvLookupOutput,    ToolData,    ValidationInput,)from workflows import workflow_helpers as helpersfrom workflows.workflow_helpers import (    LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,    LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,)with workflow.unsafe.imports_passed_through():    from activities.activities import AgentActivities    from models.requests import CombinedInput, ToolPromptInput    from prompts.agent_prompt_generators import generate_genai_prompt# ConstantsMAX_TURNS_BEFORE_CONTINUE = 250

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

agent and its goal, 250 turns should be an adequate numberDefining the agent class and constructorYou define a Temporal Workflow by creating a Python class. Createthe AgentGoalWorkflow class, decorate it with@workflow.defn, and define the __init__ method:
Your Workflow must be decorated with the @workflow.defndecorator. This is what distinguishes it as a Temporal Workflow.While a Workflow isn't required to have a __init__ method, youragent will benefit from instance variables.@workflow.defnclass AgentGoalWorkflow:    """Workflow that manages tool execution with user confirmation and conversation history."""    def __init__(self) -> None:        self.conversation_history: ConversationHistory = ```
{"messages": []}
```        self.prompt_queue: Deque[str] = deque()        self.chat_ended: bool = False        self.tool_data: Optional[ToolData] = None        self.goal: Optional[AgentGoal] = None        self.waiting_for_confirm: bool = False        self.show_tool_args_confirmation: bool = (            True  # set from env file in activity lookup_wf_env_settings        )        self.confirmed: bool = (            False  # indicates that we have confirmation to proceed to run tool        )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 record of the entirechat conversationhistoryprompt_queueA queue maintainingtasks left for the agentto processchat_endedA boolean to determineif the chat has ended ornottool_dataA record of the currenttool datagoalThe agent's goalwaiting_for_confirmA boolean signifying ifthe agent is ready toexecute the toolshow_tool_args_confirmationA boolean to determineif extra confirmation isnecessary beforeexecuting toolsconfirmedA boolean fordetermining if the agentis confirmed to proceed

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, you'll begin implementing the main Workflow method.Defining the agent control variablesEvery Temporal Workflow has a singular entry point, also known asthe Workflow method. This method is decorated with the@workflow.run decorator. Your Workflow method will contain theprimary business logic for your agent.Declare the method header for your agent's Workflow method:
The Workflow method must be decorated with the@workflow.run decorator, and must be implemented usingPython's asyncio library. This method takes in one argument, atype you defined named CombinedInput, and returns a str.Recall that CombinedInput contains the AgentGoal andAgentGoalWorkflowParams types.Add the next few lines of code to the run method to assign valuesto a few parameters:    @workflow.run    async def run(self, combined_input: CombinedInput) -> str:
        """Main workflow execution method."""        # setup phase, starts with blank tool_params and agent_goal prompt as defined in tools/goal_registry.py        params = combined_input.tool_params        self.goal = combined_input.agent_goal        await self.lookup_wf_env_settings()

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The last line calls a method, lookup_wf_env_settings, thathasn't been defined yet, so define that as a method within theAgentGoalWorkflow class but not within the scope of your runmethod:
This method invokes the get_wf_env_vars Activity to read theenvironment variables and store them appropriately.Next, add the final lines of code to finish instantiating the instanceand local variables within the run method:    # look up env settings in an activity so they're part of history    async def lookup_wf_env_settings(self) -> None:        env_lookup_input = EnvLookupInput(            show_confirm_env_var_name="SHOW_CONFIRM",            show_confirm_default=True,        )        env_output: EnvLookupOutput = await workflow.execute_activity_method(            AgentActivities.get_wf_env_vars,            env_lookup_input,            start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,            retry_policy=RetryPolicy(                initial_interval=timedelta(seconds=5), backoff_coefficient=1            ),        )        self.show_tool_args_confirmation = env_output.show_confirmCheckpoint: Your file should currently look like this:

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

If the parameters include a prompt, they are added to theprompt_queue for the agent to process. The prompt_queue issource of truth for tasks that the agent needs to execute tocomplete its goal. Tasks will be added throughout the lifecycle,which will drive execution forward.Finally, you set the waiting for confirmation variable to false andthe current tool to None. These variables will change as the agentprocesses the various tasks to complete its goal.Now that you've defined the class and instantiated the controlvariables, you can build the core agent loop.Implementing the core agent loopThe core of the agent's logic, processing, and validation takesplace within a single main loop. Every iteration of the loop isconsidered a turn. The agent may perform an action in a turn, orset up an action to be performed on the next turn, and continuethe loop to end its turn. This loop will run indefinitely until theagent determines it achieved its goal and returns the final result.Handling the await conditions and exit conditionThe first step is to create the loop and handle the await and exitconditions. Add the following lines of code within the run method        if params and params.prompt_queue:            self.prompt_queue.extend(params.prompt_queue)        waiting_for_confirm: bool = False        current_tool: Optional[CurrentTool] = None

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

directly following the await self.lookup_wf_env_settings()line:
This section creates the loop, and then immediately awaits for acondition to become true so it can proceed. The conditions it'swaiting on is for either something to be added to theprompt_queue so the agent has something to process, the chatend either later in the loop or via Signal, or for the user to confirmexecution. Once any of these three conditions is met, it continuesexecution. The agent then checks to see if the self.chat_endedinstance variable is True, indicating that the agent can haltexecution. If so, the agent will return the conversation historystored in the self.conversation instance variable, and theWorkflow Execution will close.Executing the toolNext, your agent will determine if it is appropriate to execute a the        while True:            # wait indefinitely for input from signals - user_prompt, end_chat, or confirm as defined below            await workflow.wait_condition(                lambda: bool(self.prompt_queue) or self.chat_ended or self.confirmed            )            # handle chat should end. When chat ends, push conversation history to workflow results.            if self.chat_ended:                return f"```
{self.conversation_history}
```"

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

tool, and if it is, invoke an Activity to do so.Continue by adding the following code to execute the tool:
Before the agent executes a tool, the agent confirms that the toolmeets the requirements for execution and that the current tool isnot None. If both of these checks evaluate to True, the agentexecutes the tool. Once the tool has completed execution, itcontinues the loop, meaning it skips all further execution andreturns to the top of the loop, ready to begin another iteration.Adding in a few more helper methodsNext, implement three helper method that the tool execution codeblock called, but had not yet implemented.The first checks if the tool is ready for execution. Leave the runand append this new method to your class:            # Execute the tool            if self.ready_for_tool_execution() and current_tool is not None:                await self.execute_tool(current_tool)                continue
    # define if we're ready for tool execution    def ready_for_tool_execution(self) -> bool:        return (            self.confirmed and self.waiting_for_confirm and self.tool_data is not None        )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This method checks if the user confirmed execution viaself.confirmed, if the agent has confirmed it has the data itneeds to execute via self.waiting_for_confirm, and ifself.tool_data is set. If this evaluates to True, the tool isready for execution and the method returns True.The second method executes the tool. Leave the run and appendthis new method to your class:    # execute the tool - set self.waiting_for_confirm to False if we're not waiting for confirm anymore    # (always the case if it works successfully)    async def execute_tool(self, current_tool: CurrentTool) -> None:        workflow.logger.info(            f"workflow step: user has confirmed, executing the tool ```
{current_tool}
```"        )        self.confirmed = False        confirmed_tool_data = self.tool_data.copy()        confirmed_tool_data["next"] = "confirm"        self.add_message("user_confirmed_tool_run", confirmed_tool_data)        # execute the tool by key as defined in tools/__init__.py        await helpers.handle_tool_execution(            current_tool,            self.tool_data,            self.add_message,            self.prompt_queue,        )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This method resets the self.confirmed variable, makes a copyof the tool data to then modify, and adds a message to theconversation history with this modified tool data. It then uses thehandle_tool_execution function to invoke the tool as anActivity. Once the Activity has completed, it returns thewaiting_for_confirm variable. On a successful execution, theself.waiting_for_confirm instance variable is set to False,resetting it and preparing the agent for its next turn in theconversation.And finally, the execute_tool helper method called yet anotherhelper method, the add_message method. This method addsmessages to the conversation history.        self.waiting_for_confirm = False
    def add_message(self, actor: str, response: Union[str, Dict[str, Any]]) -> None:        """Add a message to the conversation history.        Args:            actor: The entity that generated the message (e.g., "user", "agent")            response: The message content, either as a string or structured data        """        if isinstance(response, dict):            response_str = str(response)            workflow.logger.debug(f"Adding ```
{actor}
``` message: ```
{response_str[:100]}
```...")        else:            workflow.logger.debug(f"Adding ```
{actor}
``` message: ```
{response[:100]}
```...")

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The method checks to see if the response parameter passed in isa dict or str. It then removes the first 100 characters, whichcontain boilerplate LLM response, and adds the message to theself.conversation_history instance variable.Validating user promptsBefore processing any input from the user, the agent needs tovalidate it. You defined Activities in a prior section to validate thedata, and now your Workflow will invoke them.Continue by adding the prompt processing logic within the coreagent loop:        self.conversation_history["messages"].append(            ```
{"actor": actor, "response": response}
```        )
Checkpoint: Your file should currently look like this:
            # process forward on the prompt queue if any            if self.prompt_queue:                # get most recent prompt                prompt = self.prompt_queue.popleft()                workflow.logger.info(                    f"workflow step: processing message on the prompt queue, message is ```
{prompt}
```"                )                # Validate user-provided prompts                if helpers.is_user_prompt(prompt):                    self.add_message("user", prompt)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The validation code first checks to see if there are any prompts in                    # Validate the prompt before proceeding                    validation_input = ValidationInput(                        prompt=prompt,                        conversation_history=self.conversation_history,                        agent_goal=self.goal,                    )                    validation_result = await workflow.execute_activity_method(                        AgentActivities.agent_validatePrompt,                        args=[validation_input],                        schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,                        start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,                        retry_policy=RetryPolicy(                            initial_interval=timedelta(seconds=5), backoff_coefficient=1                        ),                    )                    # If validation fails, provide that feedback to the user - i.e., "your words make no sense, puny human" end this iteration of processing                    if not validation_result.validationResult:                        workflow.logger.warning(                            f"Prompt validation failed: ```
{validation_result.validationFailedReason}
```"                        )                        self.add_message(                            "agent", validation_result.validationFailedReason                        )                        continue

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

the queue. If so, it removes the most recent prompt for processing.Next is calls the is_user_prompt helper function you definedearlier to determine who the author of the prompt is. If the promptis from the agent, the validation step is skipped. However, if theprompt is from a user, it is validated. The agent creates aValidationInput variable containing the prompt, theconversation history, and the agent's goal. The agent thenexecutes the agent_validatePrompt Activity, passing theValidationInput variable as input. If the validation passes, theWorkflow proceeds execution. However, if the validation fails, theagent logs the error, adds it to conversation history and, resets tothe beginning using continue, where it will inform the user of theerror and await a response.It's important to recall that within agent_validatePrompt,regardless of success the Activity calls the agent_toolPlannermethod. This provides a reason why the validation failed, ifnecessary.Generating a context-aware promptUpon successful validation, the Workflow invokes another Activityto generate a context-aware prompt for the LLM to use.Continue by adding the call to the generate_genai_promptfunction you implemented in the prompts submodule to yourcode:                # If valid, proceed with generating the context and prompt                context_instructions = generate_genai_prompt(                    agent_goal=self.goal,                    

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This function call takes the agent's goal, the current conversationhistory, and the tool's data as input to generate the prompt. Recallthat the tool data may be blank, for example, on the first iterationas a tool hasn't been selected. The prompt template handles thisand only renders the data if it exists.Executing the tool plannerNow that the prompt is constructed, you can use the LLM to planwhich tool to use.Add the following code call the agent_toolPlanner Activity andprocess the results:conversation_history=self.conversation_history,                    raw_json=self.tool_data,                )
                prompt_input = ToolPromptInput(                    prompt=prompt, context_instructions=context_instructions                )                # connect to LLM and execute to get next steps                tool_data = await workflow.execute_activity_method(                    AgentActivities.agent_toolPlanner,                    prompt_input,                    schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,                    start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,                    retry_policy=RetryPolicy(                        initial_interval=timedelta(seconds=5), backoff_coefficient=1                    ),

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Before the agent executes the Activity, it creates a variable usingyour type ToolPromptInput that contains the prompt andcontext. It then invokes the agent_toolPlanner Activity, passingin this variable. The Activity makes a call to the LLM with theprompt to determine what tool the agent should use to proceedwith the next step of its goal, and returns the response as a dict.If the SHOW_CONFIRM environment variable was set to True, thenthe force_confirm key is also set to True. Next, theself.tool_data instance variable is updated with the datareturned from the Activity execution. It then sets the next_stepand current_tool variables to prepare for the next phase ofexecution.Determining the next_stepThe next_step variable contains the next action the LLM decidedthe agent should take to achieve its goal. This variable can onlycontain the value question, confirm, and done, which the                )                tool_data["force_confirm"] = self.show_tool_args_confirmation                self.tool_data = ToolData(**tool_data)                # process the tool as dictated by the prompt response - what to do next, and with which tool                next_step = tool_data.get("next")                current_tool: Optional[CurrentTool] = tool_data.get("tool")                workflow.logger.info(                    f"next_step: ```
{next_step}
```, current tool is ```
{current_tool}
```"                )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

agent interprets and acts on. When the value is question, theagent asks a clarifying question of the user, such as requesting amissing parameter. This is handled automatically via the prompt.However, confirm and done require custom logic.Add the following code to implement the path for these options:                # make sure we're ready to run the tool & have everything we need                if next_step == "confirm" and current_tool:                    args = tool_data.get("args", ```
{}
```)                    # if we're missing arguments, ask for them                    if await helpers.handle_missing_args(                        current_tool, args, tool_data, self.prompt_queue                    ):                        continue                    self.waiting_for_confirm = True                    # We have needed arguments, if we want to force the user to confirm, set that up                    if self.show_tool_args_confirmation:                        self.confirmed = False  # set that we're not confirmed                        workflow.logger.info("Waiting for user confirm signal...")                    # if we have all needed arguments (handled above) and not holding for a 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

If next_step is set to confirm, then the user confirmed theirchoice and the LLM has chosen to continue executing. If bothconfirm and current_tool have something assigned to them,the agent checks for missing arguments using thehandle_missing_args function. Remember that if thehandle_missing_args function determines an argument ismissing, it adds a new prompt to the prompt_queue so the agentasks the user on the next turn. If an argument is missing, theprompt is added and the agent continues, leading to the userbeing asked for the missing argument. If no argument is missing,then self.waiting_for_confirm is set to True, whichindicates that the agent is ready to execute the tool.It then checks if self.show_tools_args_confirmation wasset. If so, self.confirmed is set to False, forcing the user toconfirm again on the next turn. Otherwise, self.confirmed isdebugging confirm, proceed:                    else:                        self.confirmed = True                # else if the next step is to be done with the conversation such as if the user requests it via asking to "end conversation"                elif next_step == "done":                    self.add_message("agent", tool_data)                    # here we could send conversation to AI for analysis                    # end the workflow                    return str(self.conversation_history)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

set to True, and the user approved the tool execution on the nextturn.However, if next_step is set to done, the LLM determined thatthe goal is complete, and no more work is necessary. The agentwraps up by adding a final message to the conversation history,and then returns the conversation history, closing the WorkflowExecution.Handling a long running executionThe final segment of the agent loop handles long runningexecution. Temporal Workflows have a limit on the size of a singleWorkflow Execution's Event History. If the Event History is too long,then the agent should perform a Continue-As-New operation toprevent a potential failure.Add the following code to check and execute a Continue-As-Newif necessary:
First, the current tool data is added to the conversation history.Before, you defined a helper functioncontinue_as_new_if_needed to determine if the Workflow                self.add_message("agent", tool_data)                await helpers.continue_as_new_if_needed(                    self.conversation_history,                    self.prompt_queue,                    self.goal,                    MAX_TURNS_BEFORE_CONTINUE,                    self.add_message,                )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

should perform the Continue-As-New operation. This functionmakes its decision based on the number of turns the agentcompleted prior to calling the function. If it is greater, then theagent performs the Continue-As-New operation.Finally, you are going to implement a method for external TemporalClients to send and retrieve information to and from the WorkflowExecution while it's running.Communicating with the WorkflowTemporal Workflows allow data to be sent and retrieved during arunning execution. These features are known as Signals andQueries.Look back at the core event loop in the Workflow, specifically theawait line at the very top of the loop:
You may have noticed the chat_ended variable was neverchanged, or the user's input was never added to theprompt_queue. This is done via sending Signals to your runningCheckpoint: Your file should currently look like this:
        while True:            # wait indefinitely for input from signals - user_prompt, end_chat, or confirm as defined below            await workflow.wait_condition(                lambda: bool(self.prompt_queue) or self.chat_ended or self.confirmed            )

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Workflow Execution.Accepting the users inputTo accept user input and add it to the prompt_queue, define aSignal handler as a method within youragent_goal_workflow.py file, outside of the run function, andunderneath your other helper functions.Add the Signal handler to your code:
A Signal handler is an async method that is decorated with the@workflow.signal decorator. When the Signal is received, it islogged, and then the agent checks to see if the chat has ended. Ifit has, the Signal is dropped as no more processing work shouldtake place. This is important, as it handles the edge case of thesmall amount of time between when the agent finishes, but prior tothe Workflow Execution closing. Then the prompt is added to theend of the prompt_queue for the agent to eventually process.    # Signal that comes from api/main.py via a post to /send-prompt    @workflow.signal    async def user_prompt(self, prompt: str) -> None:        """Signal handler for receiving user prompts."""        workflow.logger.info(f"signal received: user_prompt, prompt is ```
{prompt}
```")        if self.chat_ended:            workflow.logger.info(f"Message dropped due to chat closed: ```
{prompt}
```")            return        self.prompt_queue.append(prompt)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Confirming the users requestAnother Signal to implement is the user confirming the use of atool, specifically when SHOW_CONFIRM is set to True.Add the following Signal handler to the bottom of your file:
This code implements the Signal handler method, decorates it with@workflow.signal, and logs that the Signal was received. It thensets the self.confirmed instance variable to True, which willunblock the main agent loop.Ending the chatThe last Signal handler your agent needs is to allow the user to endthe chat.Add the following Signal handler to the bottom of your file:    # Signal that comes from api/main.py via a post to /confirm    @workflow.signal    async def confirm(self) -> None:        """Signal handler for user confirmation of tool execution."""        workflow.logger.info("Received user signal: confirmation")        self.confirmed = True
    # Signal that comes from api/main.py via a post to /end-chat    @workflow.signal    async def end_chat(self) -> None:        """Signal handler for ending the chat session."""

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Similar to the previous Signal handler, this is a decorated methodthat sets an instance variable to True, in this case theself.chat_ended variable.Sending information to a Workflow may not be the only action youwant to do. You may also want to retrieve some information duringits execution. Temporal provides this capability with Queries.Retrieving the conversing historyImplementing a Query is similar to implementing a Signal: Youdefine a method and decorate it. However, the method can't beasync, and the decorator is @workflow.query.Add the following Query to the bottom of your file, to retrieve theconversation history:
This Query returns the current conversation history that is storedin the self.conversation_history instance variable.Retrieving the latest tool dataThe final Query returns the latest tool data.        workflow.logger.info("signal received: end_chat")        self.chat_ended = True
    @workflow.query    def get_conversation_history(self) -> ConversationHistory:        """Query handler to retrieve the full conversation history."""        return self.conversation_history

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Add the following code to the bottom of your file to implement it:
This Query returns the current tool data, if available, that is storedin the self.tool_data instance variable.Your Workflow now has the necessary Signals and Queries for aclient API to properly communicate with it and implement a userinterface on top of it.
This Workflow demonstrates the key patterns for building durableAI agents. It is event-driven, handling interactions with Signals andQueries, it validates user prompts and implements guardrails, itrequires confirmation for tool execution, it maintains state andcontext across failures, and it's observable. The duration of theWorkflow Execution is irrelevant. Thanks to Temporal, the sessioncould go on for minutes, hours, days, or even weeks.    @workflow.query    def get_latest_tool_data(self) -> Optional[ToolData]:        """Query handler to retrieve the latest tool data response if available."""        return self.tool_data
The workflows/agent_goal_workflow.py is completeand will need no more revisions. You can review thecomplete file and copy the code here.
Before moving on to the next section, verify your files anddirectory structure is correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

In the next section, you will implement the Temporal Worker, whichis responsible for executing your Workflow and Activities.Building the TemporalWorkerTemporal Workflows are not run by executing theagent_goal_workflow.py file. Workflows, Activities, Signal andQuery handling, and all Temporal operations are handled byTemporal Workers.Creating the Temporal clientA Worker uses a Temporal client to communicate with theTemporal service to coordinate execution. A Temporal client is alsoused to request execution of Temporal Workflows. Since thisapplication will require multiple Temporal clients, you willimplement a shared submodule that others can call to create aTemporal client. This reduces the need for duplicate code andpotentially incorrectly setting the Task Queue.First, create the shared directory and a blank __init__.py fileto create the submodule:Next, create the file config.py within the shared directory andadd the following import statements:mkdir sharedtouch shared/__init__.py
```
import os

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

You'll then load in the environment variables you specified earlier. Ifyou are running this tutorial using the local development server,these are commented out in your .env file and will use the defaultsettings.
Finally, add the code to configure a Temporal client:import osfrom dotenv import load_dotenvfrom temporalio.client import Clientfrom temporalio.service import TLSConfig
load_dotenv(override=True)# Temporal connection settingsTEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "agent-task-queue")# Authentication settingsTEMPORAL_TLS_CERT = os.getenv("TEMPORAL_TLS_CERT", "")TEMPORAL_TLS_KEY = os.getenv("TEMPORAL_TLS_KEY", "")TEMPORAL_API_KEY = os.getenv("TEMPORAL_API_KEY", "")async def get_temporal_client() -> Client:    """    Creates a Temporal client based on environment configuration.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

    Supports local server, mTLS, and API key authentication methods.    """    # Default to no TLS for local development    tls_config = False    print(f"Address: ```
{TEMPORAL_ADDRESS}
```, Namespace ```
{TEMPORAL_NAMESPACE}
```")    print("(If unset, then will try to connect to local server)")    # Configure mTLS if certificate and key are provided    if TEMPORAL_TLS_CERT and TEMPORAL_TLS_KEY:        print(f"TLS cert: ```
{TEMPORAL_TLS_CERT}
```")        print(f"TLS key: ```
{TEMPORAL_TLS_KEY}
```")        with open(TEMPORAL_TLS_CERT, "rb") as f:            client_cert = f.read()        with open(TEMPORAL_TLS_KEY, "rb") as f:            client_key = f.read()        tls_config = TLSConfig(            client_cert=client_cert,            client_private_key=client_key,        )    # Use API key authentication if provided    if TEMPORAL_API_KEY:        print(f"API key: ```
{TEMPORAL_API_KEY}
```")        return await Client.connect(            TEMPORAL_ADDRESS,            namespace=TEMPORAL_NAMESPACE,            api_key=TEMPORAL_API_KEY,            tls=True,  # Always use TLS with API key        )    # Use mTLS or local connection    return await Client.connect(        TEMPORAL_ADDRESS,

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This code checks whether or not you configured TLS certs forsecure connection or a Temporal API key for connection toTemporal Cloud. It then returns a configured Temporal client, readyto communicate with the Temporal service.Configuring the WorkerNow that you have a reusable way of creating a Temporal client,you can use that to configure your Temporal Worker.Start by creating the worker directory:Then, create the file worker.py in the worker directory and addthe following import statements:        namespace=TEMPORAL_NAMESPACE,        tls=tls_config,    )
mkdir worker
import asyncioimport concurrent.futuresimport loggingimport osfrom dotenv import load_dotenvfrom temporalio.worker import Workerfrom activities.activities import AgentActivities, dynamic_tool_activityfrom shared.config import TEMPORAL_TASK_QUEUE, get_temporal_clientfrom workflows.agent_goal_workflow import 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

These import statements include libraries from the standardlibrary, third-party packages such as dotenv and thetemporalio.worker library, as well as a few of the libraries youimplemented. A Worker must register the Workflows and Activitiesit intends to execute, so it must import them, as well as thefunction for creating the Temporal client.Next, create the main method and add the code responsible forinitializing a few variables, including creating the Temporal clientand creating an instance of your AgentActivities class.AgentGoalWorkflow
async def main():    # Load environment variables    load_dotenv(override=True)    # Print LLM configuration info    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4")    print(f"Worker will use LLM model: ```
{llm_model}
```")    # Create the client    client = await get_temporal_client()    # Initialize the activities class    activities = AgentActivities()    print(f"AgentActivities initialized with LLM model: ```
{llm_model}
```")    print("Worker ready to process tasks!")    logging.basicConfig(level=logging.WARN)

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This code loads the in the environment variables from your .envfile. It uses the LLM_MODEL environment variable to print whichmodel the agent will call, defaulting to OpenAI's GPT-4 if none isset. It then creates a Temporal client, and an instance of yourAgentActivities class before setting the log level to WARN.Finally, add the code to configure and start your Worker:
The code creates a ThreadPoolExecutor for the Worker to useas the activity_executor. Since an agent's tools can be either    # Run the worker    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:        worker = Worker(            client,            task_queue=TEMPORAL_TASK_QUEUE,            workflows=[AgentGoalWorkflow],            activities=[                activities.agent_validatePrompt,                activities.agent_toolPlanner,                activities.get_wf_env_vars,                dynamic_tool_activity,            ],            activity_executor=activity_executor,        )        print(f"Starting worker, connecting to task queue: ```
{TEMPORAL_TASK_QUEUE}
```")        print("Ready to begin processing...")        await worker.run()if __name__ == "__main__":    asyncio.run(main())

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

async or not, you must use one of the synchronous safe methodsfor Activity execution. You can read more about this in the PythonSDK documentation.Next, the Worker object is created, passing in the client, thetask_queue, the activity_executor, and then registering theindividual Workflows and Activities the Worker can execute. TheWorker is then started with await worker.run(), which createsa long-running process that will poll the Temporal service,executing Workflow and Activities when they are requested.Finally, the standard if __name__ == "__main__" calls themain function when you run worker.py, starting the Worker.Now that you have implemented your Worker, verify that it runs.Testing the WorkerBefore starting the Worker, you need to start a Temporal service.To start the local development server, open a terminal and run thefollowing command:This starts a local Temporal service running on port 7233 with theweb UI running on port 8233. The output of this command shouldresemble (The exact version numbers may not match):temporal server start-dev
CLI 1.1.1 (Server 1.25.1, UI 2.31.2)Server:  localhost:7233UI:      http://localhost:8233Metrics: http://localhost:53697/metrics

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, open another terminal and run your Worker:Your Worker should start, and the output should be:
The command will not exit, but will persist; this is expected. It iswaiting for Workflows and Activity tasks to execute. If your Workeris running successfully, that's as much as you can test for themoment. Kill both the worker and Temporal service by pressingCTRL-C in each terminal.Next, you will implement a REST API that will serve as the backendservice for invoking your agent.uv run worker/worker.pyWorker will use LLM model: openai/gpt-4oAddress: localhost:7233, Namespace default(If unset, then will try to connect to local server)AgentActivities initialized with LLM model: openai/gpt-4oWorker ready to process tasks!Starting worker, connecting to task queue: agent-task-queueReady to begin processing...
Before moving on to the next section, verify that your filesand directory structure are correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Building a REST API forinteracting with your agentNow that you have your agent implemented, you need a way forclient applications to interact with it. Temporal provides clientlibraries, but having an API to manage invoking a Workflow,sending Signals and Queries, and managing various WorkflowExecutions is a typical pattern for managing Temporal Workflows.In this step, you will create a backend API that will serve as theinterface for interacting with your agent. You'll use the FastAPIframework to build this. FastAPI is a great choice to pair withTemporal, as it's an async Python backend that supports typehints.Setting up the FastAPI applicationFirst, create the directory structure for your FastAPI application:Next, create the API file at api/main.py and include the followingimport statements:$ mkdir api
import asynciofrom collections import dequefrom contextlib import asynccontextmanagerfrom typing import Dict, Optionalfrom dotenv import load_dotenvfrom fastapi import FastAPI, HTTPExceptionfrom fastapi.middleware.cors import 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This imports various packages from the standard library, third-party libraries including FastAPI and Temporal, and a few of yourcustom libraries. The API imported the AgentGoalWorkflow so itcan invoke it, the goal_event_flight_invoice for specificationof the goal, the get_temporal_client function andTEMPORAL_TASK_QUEUE constant for communicating with theTemporal service, and a few of your custom types for propercommunication with the Workflow.Next, add the code to configure and instantiate the FastAPI object:CORSMiddlewarefrom temporalio.api.enums.v1 import WorkflowExecutionStatusfrom temporalio.client import Clientfrom temporalio.exceptions import TemporalErrorfrom models.requests import AgentGoalWorkflowParams, CombinedInput, ConversationHistoryfrom shared.config import TEMPORAL_TASK_QUEUE, get_temporal_clientfrom tools.goal_registry import goal_event_flight_invoicefrom workflows.agent_goal_workflow import AgentGoalWorkflow
temporal_client: Optional[Client] = None@asynccontextmanagerasync def lifespan(app: FastAPI):    global temporal_client    # Create the Temporal client    temporal_client = await get_temporal_client()

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This creates a Temporal client, then uses the lifespan functionto call the get_temporal_client function. The lifespanfunction, paired with the @asynccontextmanager decoratordefines a context manager that defines startup and shutdownbehavior for your FastAPI app. Next, it creates the FastAPI app,passing in the lifespan as a parameter. Finally, you load in theenvironment variables and specify the AGENT_GOAL togoal_event_flight_invoice.Next, add the appropriate middleware for handling CORS anddefine the root handler for your app:    yieldapp = FastAPI(lifespan=lifespan)# Load environment variablesload_dotenv()AGENT_GOAL = goal_event_flight_invoice
app.add_middleware(    CORSMiddleware,    allow_origins=["http://localhost:5173"],    allow_credentials=True,    allow_methods=["*"],    allow_headers=["*"],)@app.get("/")def root() -> Dict[str, str]:    return ```
{"message": "Temporal AI Agent!"}
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The CORS settings are set up to allow for access from an originAny request to the root of your application will return JSON with asingle key and a message.Before moving on, test your FastAPI app by running the followingcommands:In one terminal, start your Temporal development server:This starts a local Temporal service running on port 7233 with theweb UI running on port 8233. The output of this command shouldresemble (The exact version numbers may not match):
In another terminal, start the API using uv from the root of yourproject:This uses uvicorn, an ASGI server to run the FastAPI app andauto reload the app if any changes are detected.The output of this command should resemble:$ temporal server start-dev
CLI 1.1.1 (Server 1.25.1, UI 2.31.2)Server:  localhost:7233UI:      http://localhost:8233Metrics: http://localhost:53697/metrics
```
$ uv run uvicorn api.main:app --reload
INFO:     Will watch for changes in these 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Next, test your application is working by sending a request to it:Your response should be:Now that you have the base FastAPI application configured with aTemporal client, you will implement the functions to interact withyour agent Workflow.Implementing agent WorkflowendpointsYour API only needs a few endpoints to communicate with theagent. You will implement the functionality to send Signals, get theconversation history, and start the Workflow.Validating the Temporal clientdirectories: ['/Users/ziggy/temporal-ai-agent']INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)INFO:     Started reloader process [31826] using StatReloadINFO:     Started server process [31828]INFO:     Waiting for application startup.Address: localhost:7233, Namespace default(If unset, then will try to connect to local server)INFO:     Application startup complete.$ curl localhost:8000```
{"message":"Temporal AI Agent!"}
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Every function will use the same Temporal client. First, you willimplement a helper function to verify the client is set up correctly.Add the following function to your main.py file:
This function ensures the global Temporal client is not None. If itisn't, the function returns the client. If it is None, it will raise anexception. This is a type-safe way of validating the client beforeevery function call.Starting the agent WorkflowNext, you'll define an endpoint that a client will use to start theagent Workflow. This endpoint is a POST endpoint, and doesn'ttake any parameters.Add the endpoint to your api.py file:def _ensure_temporal_client() -> Client:    """Ensure temporal client is initialized and return it.    Returns:        TemporalClient: The initialized temporal client.    Raises:        HTTPException: If client is not initialized.    """    if temporal_client is None:        raise HTTPException(status_code=500, detail="Temporal client not initialized")    return temporal_client

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

The code verifies the Temporal client, then creates aCombinedInput type containing an AgentGoalWorkflowParamsobject and the AGENT_GOAL. The AgentGoalWorkflowParamsobject assigns None to its first attribute, which represents theconversation history. This is fine, as there is currently noconversation history. The second attribute is the first prompt the@app.post("/start-workflow")async def start_workflow() -> Dict[str, str]:    """Start the AgentGoalWorkflow"""    temporal_client = _ensure_temporal_client()    # Create combined input    combined_input = CombinedInput(        tool_params=AgentGoalWorkflowParams(            None, deque([f"### ```
{AGENT_GOAL.starter_prompt}
```"])        ),        agent_goal=AGENT_GOAL,    )    workflow_id = "agent-workflow"    # Start the workflow with the starter prompt from the goal    await temporal_client.start_workflow(        AgentGoalWorkflow.run,        combined_input,        id=workflow_id,        task_queue=TEMPORAL_TASK_QUEUE,    )    return ```
{        "message": f"Workflow started with goal's starter prompt: {AGENT_GOAL.starter_prompt}
```."    }

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

agent will execute. You then specify the workflow_id that willidentify the execution, in this case it is hard coded to 
agent-
workflow. Finally, you start the Workflow asynchronously usingtemporal.client.start_workflow, specifying the Workflowmethod AgentGoalWorkflow.run, the parametercombined_input, workflow_id, and task_queue.The function then returns with a message stating that theWorkflow has started.Sending a user prompt to the WorkflowNow you'll implement sending the user's prompt to the Workflow.The user will interact with the chatbot interface, sending messagesto the agent. The chatbot sends these as Signals to theuser_prompt Signal handler you defined in your Workflow.Add the following code to send the user's prompt to the Workflow:
This code identifies the Workflow Execution by its workflow_id,@app.post("/send-prompt")async def send_prompt(prompt: str) -> Dict[str, str]:    """Sends the user prompt to the Workflow"""    temporal_client = _ensure_temporal_client()    workflow_id = "agent-workflow"    handle = temporal_client.get_workflow_handle(workflow_id)    await handle.signal("user_prompt", prompt)    return ```
{"message": f"Prompt '{prompt}
```' sent to workflow ```
{workflow_id}
```."}

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

and sends the user's prompts sent to the API as Signals to thatWorkflow Execution.Sending a confirmation to the WorkflowIf you have the SHOW_CONFIRM option set in your .env file, thenthe user must confirm the tool before it is executed. This choice issent to the workflow via a Signal. You already implemented theSignal handler in the Workflow, now you will implement sending theSignal.Add the following code to send the confirm Signal:
This code identifies the Workflow Execution by its workflow_id,and sends the Signals sent to the API to that Workflow Execution.Ending the chatFinally, the user can choose to end the chat at any time by sayingsomething along the lines of "end conversation." You alsoimplemented this Signal handler in your Workflow, so now you'llimplement the sending of the Signal.@app.post("/confirm")async def send_confirm() -> Dict[str, str]:    """Sends a 'confirm' signal to the workflow."""    temporal_client = _ensure_temporal_client()    workflow_id = "agent-workflow"    handle = temporal_client.get_workflow_handle(workflow_id)    await handle.signal("confirm")    return ```
{"message": "Confirm signal sent."}
```

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Add the following code:
This code identifies the Workflow Execution by its workflow_id,and sends the Signals sent to the API to that Workflow Execution.Retrieving the conversation historyThe last API endpoint you must implement retrieves theconversation history. The UI uses this to populate the interface forthe user to read. This API will perform a Query and retrieve theinformation from the running Workflow Execution.Add the following code to implement the endpoint:@app.post("/end-chat")async def end_chat() -> Dict[str, str]:    """Sends a 'end_chat' signal to the workflow."""    temporal_client = _ensure_temporal_client()    workflow_id = "agent-workflow"    handle = temporal_client.get_workflow_handle(workflow_id)    await handle.signal("end_chat")    return ```
{"message": "End chat signal sent."}
```
@app.get("/get-conversation-history")async def get_conversation_history() -> ConversationHistory:    """Calls the workflow's 'get_conversation_history' query."""    temporal_client = _ensure_temporal_client()    try:        handle = temporal_client.get_workflow_handle("agent-

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

workflow")        failed_states = [            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_TERMINATED,            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_CANCELED,            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_FAILED,        ]        description = await handle.describe()        if description.status in failed_states:            print("Workflow is in a failed state. Returning empty history.")            return []        # Set a timeout for the query        try:            conversation_history = await asyncio.wait_for(                handle.query("get_conversation_history"),                timeout=5,  # Timeout after 5 seconds            )            return conversation_history        except asyncio.TimeoutError:            raise HTTPException(                status_code=404,                detail="Temporal query timed out (worker may be unavailable).",            )    except TemporalError as e:        error_message = str(e)        print(f"Temporal error: ```
{error_message}
```")        # If worker is down or no poller is available, return a 404        if "no poller seen for task queue recently" in 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

This function identifies the Workflow by its Workflow ID, thenchecks the Workflow Execution's status, making sure it isn't in afailed state. It then performs the Query, setting a timeout of fiveseconds, handling various errors as they may occur. If theWorkflow Execution isn't found however, the endpoint will actuallykick it off.
You just implemented an API allowing client programs to interactwith your agent.error_message:            raise HTTPException(                status_code=404, detail="Workflow worker unavailable or not found."            )        if "workflow not found" in error_message:            await start_workflow()            return []        else:            # For other Temporal errors, return a 500            raise HTTPException(                status_code=500, detail="Internal server error while querying workflow."            )
The api/main.py is complete and will need no morerevisions. You can review the complete file and copy thecode hereBefore moving on to the next section, verify your files anddirectory structure is correct.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

In the next step, you will test your agent using a chatbot webinterface.Running your agentNow that you have implemented a mechanism of communicationfor your agent, it's time to test it. You will now download a Reactfrontend that implements a chatbot UI to interact with your agent.The UI will open in a terminal window and prompt the user with amessage stating their purpose and instructing the user what to donext. Throughout the conversation, the user will interact with theagent, responding to questions from the agent as the agent tries toaccomplish its goal.Adding a Chatbot Web UITo get started, download the pre-built React based web UI:
Once downloaded, extract the files from the zip to your rootdirectory. You can do this with your OS's tool, or with a commandline tool like unzip:Next, change directories into the frontend directory that was justextracted and install the packages to run the UI:$ curl -o frontend.zip https://raw.githubusercontent.com/temporal-community/tutorial-temporal-ai-agent/main/frontend.zip
```
$ unzip frontend.zip

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Once the packages are finished installing, the web UI is ready tointeract with your API.Starting Your AgentYou now have assembled all the pieces to run the agent tocompletion. Running the agent requires a minimum of fourdifferent terminals, however there will only be one Worker processrunning. You can either open multiple terminals, or use a terminalmultiplexer like screen or tmux. This tutorial can function with asingle Worker. However, as with all real-world Temporaldeployments, it is always better to run multiple Workers for scalingand redundancy."The first requirement is running a local Temporal server thatcoordinates workflow execution and provides durabilityguarantees.In the first terminal, start the development server:This starts a local Temporal service running on port 7233 with theweb UI running on port 8233. The output of this command shouldresemble (The exact version numbers may not match):$ cd frontendnpm install
```
$ temporal server start-dev
CLI 1.1.1 (Server 1.25.1, UI 2.31.2)Server:  localhost:7233

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

In the second terminal, start your Worker:You should see the following output output:
If you are able, running a second Worker in another terminal isrecommended using the steps above.Next, open another terminal and run the FastAPI application:This uses uvicorn, an ASGI server to run the FastAPI app andauto-reload the app if any changes are detected.The output of this command should resemble:UI:      http://localhost:8233Metrics: http://localhost:53697/metricsuv run worker/worker.pyWorker will use LLM model: openai/gpt-4oAddress: localhost:7233, Namespace default(If unset, then will try to connect to local server)AgentActivities initialized with LLM model: openai/gpt-4oWorker ready to process tasks!Starting worker, connecting to task queue: agent-task-queueReady to begin processing...
```
$ uv run uvicorn api.main:app --reload
INFO:     Will watch for changes in these 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Finally, open the last new terminal, change directories into thefrontend directory and start the web UI:You will see output to your terminal, and then your web browserwill open to localhost:5173 with your agent running.NOTEWhen first starting the web UI, you may see a red errorbanner appear upon startup with a message about timeouts.This is expected, as the UI begins polling immediately beforethe Workflow may begin. This will go away within a fewseconds once the Workflow Execution has started and thefirst message from the agent appears.Finally, open a new browser tab and navigate to localhost:8233.This will display the Temporal Web UI. You should see a runningWorkflow Execution there with the Workflow ID agent-workflow.INFO:     Will watch for changes in these directories: ['/Users/ziggy/temporal-ai-agent']INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)INFO:     Started reloader process [31826] using StatReloadINFO:     Started server process [31828]INFO:     Waiting for application startup.Address: localhost:7233, Namespace default(If unset, then will try to connect to local server)INFO:     Application startup complete.
```
$ cd frontendnpx vite

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Click on the link to open it so you can watch the Workflow progressas you run test your agent.Testing the complete systemWith all components running, you can now test the agentWorkflow.Navigate back to localhost:5173. You should see a messagesimilar to the following. Remember, the agent's responses arepowered by an LLM, so the responses are non-deterministic,meaning they are likely to be slightly different every time.
Test the conversation by responding with a city you'd like to travelto and the month you want to travel:The agent will process receive your prompt and use the LLM todetermine the next step:Agent: Welcome! I'm here to help you plan your travel to events in North America. I can assist you in finding events, booking flights, and generating invoices for your trip. To get started, please tell me which city and month you're interested in traveling to?
You: I'd like to see events in San Francisco in March
Agent: Let's proceed with finding events in San Francisco in March.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

It will determine that it should use the FindEvents tool andsearch for events.NOTEIf you have the SHOW_CONFIRM environment variable set toTrue, the UI will prompt you to confirm execution of this tooland all future tool executions. By default this is enabled, soyou will need to confirm the execution.Once you have confirmed the tool execution, the agent executesthe tool and provides events for you to choose from:
You can then respond with which event you'd like to attend:However, you forgot to provide the departure city here, which theagent recognized and then prompted you for again.Agent: I found a couple of events in San Francisco:1. Lunar New Year Festival & Parade from February 8 to February 22, 20262. San Francisco International Film Festival from April 17 to May 1, 2026Would you like to search for flights to attend any of these events? If so, please provide your departure city.You: I would like to attend the San Francisco International Film Festival
Agent: Great choice! The San Francisco International Film Festival is from April 17 to 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

Thinking about lunch, you accidentally input your lunch order intothe chatbot:The agent's guardrails recognize this isn't valid for its goal, so itinforms you and prompts you to enter your departure city.
You then provide it with your departure city:The agent now has the information it needs, and can move on tothe next step. However, it may decide to confirm with you again toensure that's what you meant.May 1, 2026. Please provide your departure city so I can search for flights.
I would like to order two double cheeseburgers.
Agent: Your request to order two double cheeseburgers doesn't align with our current goal. We're working on organizing a trip for you to attend the San Francisco International Film Festival. To proceed, please let me know your departure city so I can search for flights for your trip.You: I'm sorry. I'd like to depart from Austin, TX
Agent: Thanks! You're departing from Austin, TX. Would you like to proceed with searching for 

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

To which you should either confirm or deny. In this instance,confirm:This extra confirmation step may not always happen. It depends ifthe LLM decides to verify.However, it is now satisfied and is ready to execute the next tool.This is evident because after this response, you are asked toconfirm execution for the SearchFlights tool:
After you confirm the tool usage, the agent then executes the tool,searching for flights to your destination.NOTEIf you have supplied a RAPIDAPI key, this will make a call to amicroservice to check for real flight data. If the API returnsmultiple times with an error or no flights, this is the externalAPI being unreliable and returning sporadic error messages.To alleviate this, use the mocked function instead.Once the agent finds flight options, it will present them to you,allowing you to select a flight if there are multiple. It will promptflights from Austin to San Francisco for the San Francisco International Film Festival?
You: Yes
Agent: Let's proceed with searching for flights from Austin, TX (AUS) to San Francisco (SFO) around the dates of April 17 to May 1, 2026.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

you if you would like to create an invoice for the flight:
To which you confirm:And the agent will proceed with creating an invoice, prompting theuser to allow the execution of the CreateInvoice tool:The agent then creates the invoice, the goal is complete, and thechat is over.
NOTEIf you set a STRIPE_API_KEY environment variable in your.env file, the tool will use the Stripe API to create an invoiceAgent: I found the cheapest flight with Southwest Airlines for $149.75. Would you like to create an invoice for this flight?You: Yes
Agent: Let's proceed with creating an invoice for the Southwest Airlines flight.
Agent: Invoice generated successfully! You can view and pay your invoice at: https://pay.example.com/invoice/12345. Your reference number is INV-12345. If you need further assistance, feel free to ask.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

in your Stripe environment. Otherwise, it will create a pseudolink.Now that the chat is over, the Workflow Execution is over. You canstart another chat session by clicking the Start New Chat buttonin the web UI, which will start a new Workflow Execution.Next, you'll examine the Event History of your most recent chatsession.Tracing the WorkflowExecution in the Web UIOne of the features of Temporal is the observability that you gainvia the Temporal Web UI. This is made possible since every eventis stored, along with the inputs and output of Workflows, Activities,and other Temporal operations.Open the Temporal Web UI at http://localhost:8233 andnavigate to your most recent run.Your UI may not look exactly like the screenshots below due todiffering UI versions, varying output from LLMs, and different userinputs. This is fine; the core concepts are still applicable.Navigate to the Workflows page to see your past agent WorkflowExecutions. This is also the default landing page.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 will see all of your completed and currently running chatsessions here. Click on the Workflow ID link agent-workflow ofthe most recently completed execution to see the details aboutthat specific execution.At the top, you'll see the summary for the Workflow Execution. Thiscontains information such as the duration of the execution, when itstarted, when it ended, what Task Queue it used, the size of thehistory, and the Workflow Type. All of this information an also bepieced together throughout the Event History, the Summarysection provides an easier way to find it.Next is the Input and Result section. Here you can see the initialinput to the Workflow, and the final result that the agent returnedin JSON format.
Below that is the Event History timeline. This is a time-basedrepresentation of every event that occurred during the executionof the Workflow.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 individual event in this timeline is expandable. You can clickon it and view the details for the event. For example, if you click ona purple Signal icon, you can see the Signal name, the identity ofthe Worker that processed it, and the input.
Other events will contain other information. Activities will containinformation regarding the timeouts, retry policies, and input andresults.Finally, you have the list version of the Event History. Everythingthat is recorded above is derived from this history. You can clickinto each individual event and see all the information about a singleevent. Certain events, such as Activities, that typically come in agroup, will be automatically paired for concise viewing as shownbelow.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 can also use this UI live. During a running Workflow Execution,you can watch live updates as you interact with your chatbot, andsee the events come in to the timeline and list views. If you'd like,run another session of your chatbot and have the web UI open in aseparate browser tab on another window so you can witness this.Next, you'll explore a few testing scenarios for demonstrating howTemporal adds durability to your agent.(Optional) Witnessing theDurability of the AgentBuilding your agent with Temporal adds durability to your agent.This means that your agent can withstand failures that traditionalapplications wouldn't be able to, such as internet outages orprocess crashes. Perform the following scenarios to witness thedurability Temporal provides.The following scenario is a simulation of one engineer's very badday at work. Follow along and see how Temporal mitigatedpotentially outage level issues.Part 1: Terminating the Worker

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 Your agent is deployed to production. You have a chatsession running, and a Worker is processing your Workflow.Suddenly, the virtual machine hosting your Worker is rebooted forupdates. The Worker is forcefully terminated and progress appearslost. What happens?Simulating this scenario:1. Ensure your Temporal development server, Worker (be sureyou only have one running), API, and web UI are running.2. Start a new chat session.3. Before typing anything in the chat, kill the Worker using 
CTRL-
C.4. Type a city and month in the chat, and press Send.5. You will see the UI stall, and not make progress. You may alsosee an error message appear at the top saying Error fetchinghistory.6. Return to the Worker terminal and restart the Worker.7. Return to the web UI and watch for progress. Eventually themessage should send and the agent Workflow progresses likenothing happened.8. If you are prompted to confirm the tool execution, do so. Thenleave the UI up for the next scenario.What happened?: When the Worker came back online, it registeredwith the Task Queue and began listening for tasks it could execute.When the original Worker timed out, not returning a response forthe task it was supposed to execute, the new Worker accepted it.The new Worker then rebuilt the state of the original WorkflowExecution, up to the point of failure, and continued execution as ifnothing happened. This new Worker could have been on anothervirtual machine within the Worker fleet, or the original Worker when

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 virtual machine finished its upgrade. This ensured that thestate was not lost and the Workflow continued to progress.Part 2: Turning off the InternetScenario: After the upgrade finished, somewhere, miles away,Danny the data center intern trips over a improperly managedpower cable and the network switch to the rack where your Workeris hosted goes down. While he scrambles to plug it back end, yourWorker is intermittently without network access. What happens?Simulating this scenario:1. Either continue from the previous session, or start with a newchat window and don't send a message yet.2. Turn off your Wifi/Unplug your network adapter to simulatethis failure.3. Respond to the prompt the agent posed to you. The agent willvalidate this using the LLM, which it won't be able to access.4. Go to your Temporal Web UI at localhost:8233 and find thefailing Activity. You will see it attempting to retry the call to theLLM.5. Turn the internet back on.6. Eventually, the LLM call will succeed, with no intervention fromthe developer.7. If you are prompted to confirm the tool execution, do so. Thenleave the UI up for the next scenario.What happened?: Temporal Activities are retried automaticallyupon failure. Intermittent failures such as network outages areoften fixed via retries. Each Activity has a default Retry Policy thatretries, then backs off increasingly to a maximum duration. Once

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal

the network comes back online, at the next retry interval the LLMcall will execute and succeed.Part 3: Swapping out LLMsScenario: Now that the switch is back online, the developer canbreath a sigh of relief. Unfortunately they get paged that theirOpenAI credits are depleted, there are angry customers trying touse the chatbot, and the only person with a corporate card toreplenish the credits is on PTO. You have an Anthropic accountwith some Claude credits you can swap in quickly.NOTEThis scenario requires an Anthropic account with a ClaudeAPI token.Simulating this scenario:1. Either continue from the previous session, or start with a newchat window. Send a few chats to make progress in theWorkflow, but do not complete it.2. Open the .env file and modify the following variables:LLM_MODEL: anthropic/claude-sonnet-4-20250514LLM_KEY: Your LLM Key3. Restart the Worker.4. Respond to the next prompt in the chat.5. The agent will respond as if nothing happened, continuing theconversation.What happened?: Since the agent is durable and preserves state,the conversation history was preserved when the Worker was

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 The state of the Workflow was reconstructed to thepoint where the Worker was terminated, and the conversationhistory was sent to Claude as context when executing the nextprompt. The agent continues executing as if nothing happened.These are just some of the failure scenarios the agent can survive.ConclusionIn this tutorial, you built a durable AI agent that handles multi-turnconversations, executes tools to achieve a goal, and recovers fromfailures. You implemented the agent using Temporal primitives,including Workflows, Activities, Signals, Queries, Workers, andTask Queues. You created a REST API to enable client integrationwith your agent. You tested your agent with a chatbot interface,and witnessed the agent survive various failure scenarios.Key architectural patternsYour implementation demonstrates several important patterns forbuilding AI agent systems:Durability through orchestration: Temporal Workflows provideautomatic state persistence, ensuring conversations surviveprocess crashes, network failures, and infrastructure issues. Thisdurability is essential for AI agents that manage long-running,stateful interactions.Separation of concerns: The architecture cleanly separatesorchestration logic (Workflows), external interactions (Activities),tool implementations (Python functions), and user interface (API),making the system maintainable and extensible.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 by design: Every execution step is recorded in theEvent History, providing visibility into the agent's execution withoutthe need for extra tools.Extensibility: The tool and goal registry pattern enables addingdefining new tools and goals without modifying the core Workflowlogic.Resources for continued learningTo continue your learning on Temporal and its use for AI, check outthe following resourcesDownload and run a more feature-rich version of this agent,which is what inspired this tutorial.Learn more about Temporal AI Use CasesExplore the Temporal documentation for more Temporalfeatures and best practices.Take a Temporal Course and dive deeper into Temporal topics.Ask a question in the Temporal community in the #topic-aichannel.Final thoughtsThe foundation you built in this tutorial enables you to build agentsto solve nearly any goal. If you're up to it, try writing your own goaland tools and have the agent execute them. Temporal's DurableExecution brings reliability and observability to long-running,distributed systems, which is exactly what AI agents are.Check back later for the next installment in this tutorial series,where you will continue to add functionality to your agent.

8/28/25, 3:47 AMHow To Build a Durable AI Agent with Temporal and Python | Learn Temporal
 updated on Jul 24, 2025 byMason Egger