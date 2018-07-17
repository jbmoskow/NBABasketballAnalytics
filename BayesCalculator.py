import pandas
import matplotlib.pyplot as plt
import numpy

def cleanDraft(stringArray):
    """Returns a list of names in the format of 1st letter of first name and last name
    e.g. Abraham Lincoln gets converted to A. Lincoln"""

    cleanedNames = []
    for n in stringArray:  # for each name

        if type(n) is str:  # ignore if blank string
            splitName = n.split()  # split up names by whitespace
            LastName = splitName[len(splitName) - 1]
            if LastName[len(LastName) - 1] == '*':  # if asterisk is in field replace with empty char.
                LastName = LastName.replace('*', '')

            cleanName = n[0] + '. ' + LastName  # store name as just '<FirstInit>. <LastName>'
            cleanedNames.append(cleanName)

    return cleanedNames


def cleanVORP(stringArray):
    """Returns a list of names in the format of 1st letter of first name and last name
    e.g. Abraham Lincoln gets converted to A. Lincoln"""

    cleanedNames = []
    for n in stringArray:  # for each name
        splitName = n.split()  # split up names by whitespace
        LastName = splitName[len(splitName) - 2]
        if LastName[len(LastName) - 1] == '*':  # if asterisk is in field replace with empty char.
            LastName = LastName.replace('*', '')

        cleanName = splitName[0] + ' ' + LastName  # store name as just '<FirstInit>. <LastName>'
        cleanedNames.append(cleanName)

    return cleanedNames


def uniqueStringFinder(stringArray):
    """Returns all unique strings in the stringArray"""

    myset = set(stringArray)
    uniqueStrings = list(myset)

    return uniqueStrings


def stringSearch(searchString, stringArray):
    """Returns a vector containing the number of instances the SearchString appears in the TargetArray"""

    matchedString = []
    if any(searchString in s for s in stringArray):
        numInstances = 1
        matchedString = searchString
    else:
        numInstances = 0

    return matchedString, numInstances


if __name__ == '__main__':
    # Perform a Bayesian Analysis of NBA Draft data

    # import data
    Draftdata = pandas.read_csv('DraftClassData_1to5.csv')
    VORPdata = pandas.read_csv('VORPdata.csv')

    # Clean Draft data
    Draftdata = Draftdata.Player  # just select the draft names only
    Draftdata = cleanDraft(Draftdata)  # convert draft player names to VORP format

    # Clean VORP data
    VORPdata = VORPdata.loc[:, '1st':'10th']  # select just the player names
    VORPdata = pandas.Series(VORPdata.values.ravel())  # concatenates the columns into one big row
    cleanedVORP = cleanVORP(VORPdata)
    VORPdata = uniqueStringFinder(cleanedVORP)  # just select the unique VORP leaders player names only

    # calc P(B|A)
    num_instances = 0
    MatchedNames = []
    for p in VORPdata:  # for each unique VORP leader
        [tempString, tempInstance] = stringSearch(p, Draftdata)
        if tempInstance == 1:
            num_instances += 1  # if VORP leader was a Top 5 draft pick add 1
            MatchedNames.append(tempString)
    P_B_A = num_instances / len(VORPdata)

    # init
    seasons = [i for i in range(1981, 2017)]  # Just look at (1980-1981 to 2015-2016 seasons) range(1981,2017)
    P_A_list = []
    P_B_list = []
    P_A_B_list = []
    num_players = []

    #  Calculate the percent of active NBA players who are also Top 5 draft picks in a given calendar year
    for year in seasons:

        filename = "AllPlayerData_" + str(year) + ".csv"
        Playerdata = pandas.read_csv(filename)

        # Clean All Player data
        Playerdata = Playerdata.Player
        cleanedPlayer = cleanDraft(Playerdata)
        Playerdata = uniqueStringFinder(cleanedPlayer)  # just select the unique players only

        num_players.append(len(Playerdata))

        MatchedNames = []
        # calc P(B)
        num_instances = 0
        for p in Draftdata:  # for each Top 5 draft pick
            [tempString, tempInstance] = stringSearch(p, Playerdata)
            if tempInstance == 1:
                num_instances += 1  # if draft pick is a current player add 1
                MatchedNames.append(tempString)

        P_B_list.append(num_instances / len(Playerdata))

    # Calculate where players in the draft are after look_ahead number of seasons
    draft_seasons = [i for i in range(1981, 2012)]  # Just look at (1980-1981 to 2011-2012 seasons) range(1981,2012)
    look_ahead = 5
    in_nba = numpy.zeros(4)
    not_in_nba = numpy.zeros(4)
    DraftFilenames = ['1to5','6to10','11to15','16to20']  # each grouping of drafted players

    for draftGroup in range(4):

        #  Just look at the current selection of draft picks
        filename = "DraftClassData_" + DraftFilenames[draftGroup] + ".csv"
        Draftdata = pandas.read_csv(filename)
        MatchedNames = []

        for year in draft_seasons:

            #  Look at player data from X seasons ahead
            filename = "AllPlayerData_" + str(year + look_ahead) + ".csv"
            Playerdata = pandas.read_csv(filename)

            # Clean All Player data
            Playerdata = Playerdata.Player
            cleanedPlayer = cleanDraft(Playerdata)
            Playerdata = uniqueStringFinder(cleanedPlayer)  # just select the unique players only

            # Clean Draft data
            CurrDraftdata = Draftdata.Player[Draftdata.DraftYear == year]  # select draft names from this year
            CurrDraftdata = cleanDraft(CurrDraftdata)  # convert draft player names to VORP format

            for p in CurrDraftdata:  # for each Top 5 draft pick in this year
                [tempString, tempInstance] = stringSearch(p, Playerdata)
                if tempInstance == 1:
                    in_nba[draftGroup] += 1  # if draft pick is still in the NBA add 1
                else:
                    not_in_nba[draftGroup] += 1
                    MatchedNames.append(p)

            for p in MatchedNames:  # check list of non-active players again in case someone missed a year
                [tempString, tempInstance] = stringSearch(p, Playerdata)
                if tempInstance == 1:
                    not_in_nba[draftGroup] -= 1
                    in_nba[draftGroup] += 1
                    MatchedNames.remove(p)

    # Plotting
    #  Graph Active players in each season
    plt.figure(1)
    plt.subplot(121)
    plt.title("Timeline of Active Players in the NBA")
    plt.plot(seasons, num_players, 'k.-')
    plt.xlabel('NBA Season')
    plt.ylabel('Number of Players')

    #  Graph percentage of Top 5 draft picks present in each season
    P_B_list_per = [i * 100 for i in P_B_list]
    plt.subplot(122)
    plt.title("Presence of Top 5 Draft Picks in NBA")
    plt.plot(seasons, P_B_list_per, 'k.-')
    plt.xlabel('NBA Season')
    plt.ylabel('Percent of Active NBA Players')
    plt.ylim([10, 20])

    # Bar Chart of 1981-2011 Draft classes (Top 20 picks) and how many players are active vs. non-active after 5 seasons
    n_groups = 4
    fig, ax = plt.subplots()

    index = numpy.arange(n_groups)
    bar_width = 0.35
    opacity = 1.0

    rects1 = ax.bar(index, (not_in_nba / (not_in_nba+in_nba))*100, bar_width,
                    alpha=opacity, color='orange')

    ax.set_xlabel('1st Round Draft Picks')
    ax.set_ylabel('Percentage of Players')
    ax.set_title('Draft Class Outcome After 5 Seasons')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('1st to 5th','6th to 10th','11th to 15th','16th to 20th'))

    fig.tight_layout()

    # calc P(A)
    P_A = (10 / numpy.mean(num_players))

    #  Calculate Bayes
    P_A_B = (P_B_A * P_A) / numpy.mean(P_B_list)

    # P(A|B) = P(B|A) * P(A) / P(B)
    # Where:
    # P(A) = probability that a NBA player is in the Top 10 in VORP for a season (prior probability)
    # P(B) = probability that a NBA player is a Top 5 draft pick
    # P(B|A) = probability that a NBA player is a Top 5 draft pick given that they are Top 10 in VORP for a season
    # P(A|B) = probability that a NBA player is in the Top 10 in VORP given that they were a Top 5 draft pick

    print("Average number of active players in the NBA across 36 seasons: %f, " % numpy.mean(num_players))
    print("Probability that an NBA Player is Top 10 in VORP: %r, " % P_A)
    print("Probability that a NBA player is a Top 5 draft pick: %r, " % numpy.mean(P_B_list))
    print("Probability that a NBA player is a Top 5 draft pick and are Top 10 in VORP: %f, " % P_B_A)
    print("Probability that a NBA player is in the Top 10 in VORP given that they were a Top 5 draft pick: %f, " % P_A_B)
    print("Draft Picks Outcome After 5 seasons:")
    for x in range(4):
        temp_per = (not_in_nba[x] / (not_in_nba[x]+in_nba[x])) * 100
        print('{0:6s} {1:3f} {2:2f} {3:2f}'.format(DraftFilenames[x],in_nba[x],not_in_nba[x],temp_per))

    plt.show()
