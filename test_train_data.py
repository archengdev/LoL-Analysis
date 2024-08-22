import pandas as pd
from sklearn.model_selection import train_test_split

def get_data(file):
    # read raw data from csv
    data = pd.read_csv(file)

    # create dataframe for data correlated to winning team
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit', 'winning_magphy', 'winning_phymit', 'winning_magphymit']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit', 'winning_magphy':'magphy', 'winning_phymit':'phymit', 'winning_magphymit':'magphymit'}))

    # create y variable for winning team (all 1's)
    oneGen = ((1 for x in range(X_win.shape[0])))
    Y_win = pd.DataFrame(oneGen, columns=['Win'])

    # create dataframe for data correlated to losing team
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit', 'losing_magphy', 'losing_phymit', 'losing_magphymit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit', 'losing_magphy':'magphy', 'losing_phymit':'phymit', 'losing_magphymit':'magphymit'}))

    # create y variable for losing team (all 0's)
    zeroGen = ((0 for x in range(X_loss.shape[0])))
    Y_loss = pd.DataFrame(zeroGen, columns=['Win'])

    # concatenate wins and losses for analysis
    Y = pd.concat([Y_win, Y_loss], ignore_index=True)
    X = pd.concat([X_win, X_loss], ignore_index=True)

    # split data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
    y_train = y_train.values.flatten()
    y_test = y_test.values.flatten()
    return X_train, X_test, y_train, y_test